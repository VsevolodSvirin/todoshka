from django.conf.urls import url

from auth.views import register, login, refresh

app_name = 'auth'


urlpatterns = [
    url(r'^register', register, name='register'),
    url(r'^login', login, name='login'),
    url(r'^refresh', refresh, name='refresh')
]
