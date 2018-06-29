from django.conf.urls import url
from django.urls import include

from api.views import router

urlpatterns = [
    url(r'auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^', include(router.urls)),
]
