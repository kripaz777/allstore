from django.urls import path,include
from rest_framework import routers
from home.views import UserViewSet,ItemViewSet,SliderViewSet,ItemFilterListView

router = routers.DefaultRouter()
router.register('user',UserViewSet)
router.register('item',ItemViewSet)

app_name = 'home'
urlpatterns=[
    path('',include(router.urls)),
    path('items/',ItemFilterListView.as_view(),name = 'items'),
]