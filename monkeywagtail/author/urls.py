from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^authors/$', views.author_list),
    url(r'^authors/(?P<slug>[-\w]+)/$', views.author_detail),
]
