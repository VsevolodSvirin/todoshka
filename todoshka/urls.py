from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('todolists.urls')),
    url(r'^auth/', include('auth.urls', namespace='auth')),
]
