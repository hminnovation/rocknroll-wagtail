from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^genres/$', views.genre_list),
    url(r'^genres/(?P<slug>[-\w]+)/$', views.genre_detail),
]
