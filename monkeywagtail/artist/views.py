# from django.shortcuts import render, get_object_or_404
# from .models import Artist


# def artist_list(request):
#     artists = Artist.objects.all()
#     return render(request, 'artist/artist_list.html', {
#         'artists': artists,
#     })


# def artist_detail(request, slug):
#     artist = get_object_or_404(Artist, slug=slug)
#     return render(request, 'artist/artist_detail.html', {
#         'artist': artist,
#     })


# def get_artist_url(self):
#     return reverse("artists:index", kwargs={"pk": self.object.pk})

from django.shortcuts import render, get_object_or_404
from monkeywagtail.feature_content_page.models import FeatureContentPage
from .models import Artist


def artist_list(request):
    artists = Artist.objects.all()
    return render(request, 'artist/artist_list.html', {
         'artists': artists,
    })


def artist_detail(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    articles = artist.artistfeaturepagerelationship_set.all().select_related("page")
    # returns `ArtistFeaturePageRelationship object` if return {{article}}
    # returns artist name if `artist.name`. So looking at wrong class?
    # But `FeatureContentPage.artists.all().select_related("page")` will throw
    # an error
    # album_artist_relationship__artist_name
    return render(request, 'artist/artist_detail.html', {
         'artist': artist,
         'article': articles,
    })

# # def get_artist_url(self):
# #     return reverse("artists:index", kwargs={"pk": self.object.pk})
