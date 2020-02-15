from django.contrib import admin
from .models import Item,Brand,SubCategory,Ad,Slider,OrderItem,Order
# Register your models here.
admin.site.register(Item)
admin.site.register(Brand)
admin.site.register(SubCategory)
admin.site.register(Ad)
admin.site.register(Slider)
admin.site.register(OrderItem)
admin.site.register(Order)
