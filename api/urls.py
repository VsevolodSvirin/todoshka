from django.conf.urls import url
from django.urls import include
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import CreateView, DetailsView

# TODO Router

urlpatterns = [
    url(r'auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^todolists/$', CreateView.as_view(), name='create'),
    url(r'todolists/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name='details'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
