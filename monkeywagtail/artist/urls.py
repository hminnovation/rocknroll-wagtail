from django.conf.urls import url
from artist.views import ArtistDetailView

urlpatterns = [
    url(r'^artists/(?P<pk>[0-9]+)/$', AuthorDetailView.as_view(), name='author-detail'),
]
