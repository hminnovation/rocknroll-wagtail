from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^artists/$', views.artist_list, name='artists'),
    url(r'^artists/(?P<slug>[-\w]+)/$', views.artist_detail),
]
