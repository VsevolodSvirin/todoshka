from django.conf.urls import url

from auth.views import login, refresh

app_name = 'auth'


urlpatterns = [
    url(r'^login', login, name='login'),
    url(r'^refresh', refresh, name='refresh')
]
