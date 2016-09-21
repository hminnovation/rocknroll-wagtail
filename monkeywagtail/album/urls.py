from django.conf.urls import url

from . import views

# @TODO
# Decide if we _really_ do want to allow albums be directly
# accessible...
app_name = 'album'
urlpatterns = [
    url(r'^albums/$', views.album_list, name='albums'),
    # url(r'^albums/(?P<slug>[-\w]+)/$', views.album_detail(), name='album'),
]
