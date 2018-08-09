from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('tasks.urls')),
    url(r'^', include('categories.urls')),
    url(r'^', include('users.urls')),
    url(r'^auth/', include('auth.urls', namespace='auth')),
]
