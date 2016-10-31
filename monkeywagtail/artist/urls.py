from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^artists/$', views.artist_list, name='artists'),
    url(r'^artists/(?P<slug>[\w-]+)/$', views.artist_detail),
    url(r'^artists/genre/(?P<genre>[\w-]+)/$', views.artist_genre_list),
]

# https://docs.djangoproject.com/en/1.10/topics/http/urls/


# \w
# When the LOCALE and UNICODE flags are not specified, matches any alphanumeric
# character and the underscore; this is equivalent to the set [a-zA-Z0-9_]. With
# LOCALE, it will match the set [0-9_] plus whatever characters are defined as
# alphanumeric for the current locale. If UNICODE is set, this will match the
# characters [0-9_] plus whatever is classified as alphanumeric in the Unicode
# character properties database.
