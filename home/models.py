from django.conf import settings
from django.db import models
from django.urls import reverse
Stock = (('In Stock','In'),('Out of Stock','Out'))
Labels = (('sale','sale'),('new','new'),('hot','hot'),('inactive','inactive'))
Status = (('active','Active'),(' ','Default'))
Categories = (('Food','Food'),('Electronics','Electronics'),('Fashion','Fashion'),('Other','Other'))
# Create your models here.
class SubCategory(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField(blank = True)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discounted_price = models.IntegerField(blank = True)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    brand = models.CharField(max_length=200,blank = True)
    slug = models.TextField()
    stock = models.CharField(max_length=100,choices = Stock,blank = True)
    labels =models.CharField(max_length=100,choices = Labels,blank = True)
    # categorys = models.CharField(max_length=100,choices=Categories,default = 1)
    # subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,default = 1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("home:product",kwargs={'slug':self.slug})

    def add_to_cart(self):
        return reverse("home:add-to-cart",kwargs={'slug':self.slug})

    def remove_single_item(self):
        return reverse("home:remove-single-item",kwargs={'slug':self.slug})

    def remove_all_item(self):
        return reverse("home:remove-all-item",kwargs={'slug':self.slug})


class Brand(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    image = models.TextField()

    def __str__(self):
        return self.title

class Ad(models.Model):
    title =models.CharField(max_length=200)
    image = models.TextField()
    rank = models.IntegerField()
    status = models.CharField(max_length=100,choices = Status)
    description = models.TextField(blank = True)

    def __str__(self):
        return self.title

class Slider(models.Model):
    title =models.CharField(max_length=200)
    image = models.TextField()
    rank = models.IntegerField()
    status = models.CharField(max_length=100,choices = Status)
    description = models.TextField(blank = True)
    uppertext = models.CharField(max_length=300)
    middletext = models.CharField(max_length=300)
    lowertext = models.CharField(max_length=300)

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.title

    def get_total_price(self):
        return self.quantity*self.item.price

    def get_total_discounted_price(self):
        return self.quantity*self.item.discounted_price

    def get_actual_price(self):
        if self.item.discounted_price>0:
            return self.get_total_discounted_price()
        else:
           return  self.get_total_price()

class  Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total_price = 0
        for orders in self.items.all():
            total_price +=orders.get_actual_price()
        return total_price

    def get_all_total_price(self):
        all_total = self.get_total() +3
        return all_total









