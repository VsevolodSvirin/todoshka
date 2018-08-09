from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from tasks.views import TaskViewSet


router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
