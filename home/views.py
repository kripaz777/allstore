from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,DetailView
from django.contrib.auth.models import User

# Importing API components
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import routers, serializers, viewsets, generics
from rest_framework.filters import OrderingFilter, SearchFilter

from .serializers import UserSerializers,ItemSerializers,SliderSerializers
# Create your views here.
# def home(request):
#
#     return render(request,'shop-index.html')
from .models import Item,Slider,Brand,Ad,Category,OrderItem,Order


class BaseView(View):
    template_context = {
        'items': Item.objects.all()
    }
    def get(self, *arg, **kwargs):
        try:
            order = Order.objects.filter(
                user=self.request.user,
                ordered=False
            )
            self.template_context['object'] = order
        except:
            return ('/')

class HomeView(BaseView):
    def get(self,request):
        self.template_context['sliders']=Slider.objects.all()
        self.template_context['brands'] = Brand.objects.all()
        self.template_context['ads'] = Ad.objects.all()
        self.template_context['category'] = Category.objects.all()

        self.template_context['new'] = Item.objects.filter(labels = 'new')
        self.template_context['sale'] = Item.objects.filter(labels='sale')
        self.template_context['hot'] = Item.objects.filter(labels='hot')

        return render(request, 'shop-index.html',self.template_context)

class ItemDetailView(DetailView):
    model = Item
    template_name = 'shop-item.html'

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug = slug)
    order_item = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )[0]
    orders = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.success(request,'The quantity is updated')
            return redirect('home:cart')

        else:
            order.items.add(order_item)
            messages.success(request,'The item is added in your cart')
            return redirect('home:cart')
    else:
        order = Order.objects.create(
            user = request.user
        )
        order.items.add(order_item)
        messages.success(request, 'The item is added in your cart')
        return redirect('home:cart')

    return render(request, 'shop-shopping-cart.html')

def remove_single_item(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    orders = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug = item.slug).exists():
            if order_item.quantity>1:
                order_item.quantity -=1
                order_item.save()
                messages.success(request,'The quantity is updated')
                return redirect('home:cart')
            else:
                messages.success(request, 'Min Quantity is 1')
                return redirect('home:cart')
        else:
            messages.success(request, 'The item Does not exists')
            return redirect('home:cart')

    return render(request, 'shop-shopping-cart.html')

def remove_all_item(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    orders = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.delete()
            messages.success(request,'The quantity is updated')
            return redirect('home:cart')

        else:
            messages.success(request, 'The item Does not exists')
            return redirect('home:cart')

    return render(request, 'shop-shopping-cart.html')



class OrderSummeryView(BaseView):
    def get(self,*arg,**kwargs):
        try:
            order = Order.objects.get(
                user = self.request.user,
                ordered = False
            )
            self.template_context['object'] = order
        except:
            return('/')

        return render(self.request,'shop-shopping-cart.html', self.template_context)

# def search(request):
#     return render(request, 'shop-search-result.html')

class Search(BaseView):
    def get(self,request):
        query = request.GET.get('query',None)
        if not query:
            return redirect('/')

        self.template_context['item_search'] = Item.objects.filter(title__icontains = query)
        self.template_context['search_for'] = query
        return render(request, 'shop-search-result.html', self.template_context)





def signup(request):
    if request.method =='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:

            if User.objects.filter(username =username).exists():
                messages.error(request,"The username is already taken")
                return redirect('home:signup')

            elif User.objects.filter(email =email).exists():
                messages.error(request,"The username is already taken")
                return redirect('home:signup')

            else:
                user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password
                )
                user.save()

        else:
            messages.error(request, "The passwords do not match ")
            return redirect('home:signup')




    return render(request,'signup.html')


# API code starts from here

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializers

class SliderViewSet(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializers

class ItemFilterListView(generics.ListAPIView):
    serializer_class = ItemSerializers
    queryset = Item.objects.all()

    filter_backends = (DjangoFilterBackend,OrderingFilter,SearchFilter)
    filter_fields = ('id','title','price','description','labels','discounted_price')
    ordering_fields = ('price','title','id','labels')
    search_fields = ('title','description')

