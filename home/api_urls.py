from django.urls import path,include
from rest_framework import routers
from home.views import UserViewSet,ItemViewSet,SliderViewSet

router = routers.DefaultRouter()
router.register('user',UserViewSet)

app_name = 'home'
urlpatterns=[
    path('',include(router.urls)),
]