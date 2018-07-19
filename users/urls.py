from django.conf.urls import url
from users.views import UserRegistrationAPIView, UserLoginAPIView


app_name = 'users'

urlpatterns = [
    url(r'^$', UserRegistrationAPIView.as_view(), name="list"),
    url(r'^login/$', UserLoginAPIView.as_view(), name="login"),
]
