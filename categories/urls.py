from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from categories.views import CategoryViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
