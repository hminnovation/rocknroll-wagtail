from django.shortcuts import render, get_object_or_404
from .models import Artist


def artist_list(request):
    artists = Artist.objects.all()
    return render(request, 'artist/artist_list.html', {
         'artists': artists,
    })


def artist_detail(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    # features = FeatureContentPage.objects.get
    # artists = Artist.objects.get
    # articles = artist.artist_related.all()
    # Line 14 - 16 can be deleted. Random ideas that didn't do what I wanted them to...
    articles = set(
            p.page for p in artist.artist_related.select_related('page').all() if p.page.live
        )
    # This works by getting pages into a list we can loop through on the template
    # It's `{classname}.{related_name}.select_related('page').all()`
    #
    # Turn below in to useful thoughts... (what didn't work)
    # If no relatedname on `artist_feature_page_relationship` is set then
    # articles = artists.artist_feature_page_relationship.all()
    # returns `ArtistFeaturePageRelationship object` if {{article}} is put in the
    # template. set() works because it steps over each page? What happens if
    # it's not a page?
    # But `FeatureContentPage.artists.all().select_related("page")` will throw
    # an error
    # album_artist_relationship__artist_name
    # Docs https://docs.djangoproject.com/en/1.10/topics/db/queries/#many-to-many-relationships
    return render(request, 'artist/artist_detail.html', {
         'artist': artist,
         'article': articles,
    })
