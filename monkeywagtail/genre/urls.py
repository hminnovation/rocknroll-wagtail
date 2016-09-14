from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^genres/$', views.genre_list),
    url(r'^genres/(?P<slug>[-\w]+)/$', views.genre_detail),
    # below doesn't work. But is getting closer to it...
    url(r'^genres/(?P<slug>[-\w]+)/(?P<sub_genre_slug>[-\w]+)/$', views.subgenre_detail),
]
