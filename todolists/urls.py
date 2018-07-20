from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from todolists.views import TodoListViewSet


router = DefaultRouter()
router.register(r'todolists', TodoListViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
