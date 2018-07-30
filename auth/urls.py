from django.conf.urls import url

from auth.views import RegisterView, LoginView, RefreshView


app_name = 'auth'


urlpatterns = [
    url(r'^register', RegisterView.as_view(), name='register'),
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^refresh', RefreshView.as_view(), name='refresh')
]
