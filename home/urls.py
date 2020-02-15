from django.urls import path

from .views import HomeView,ItemDetailView,add_to_cart,Search,signup,OrderSummeryView,remove_single_item,remove_all_item

app_name = 'home'

urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    path('product/<slug>',ItemDetailView.as_view(),name = 'product'),
    path('add-to-cart/<slug>',add_to_cart,name = 'add-to-cart'),
    path('search', Search.as_view(), name='search'),
    path('signup', signup, name='signup'),
    path('cart', OrderSummeryView.as_view(), name='cart'),
    path('remove-single-item/<slug>', remove_single_item, name='remove-single-item'),
    path('remove-all-item/<slug>', remove_all_item, name='remove-all_item'),
]
