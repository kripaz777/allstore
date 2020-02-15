from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Slider,Item

class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields=['id','username','email','first_name','lastname']

class SliderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id','title','image','description','status']

class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id','title','price','description','slug']
