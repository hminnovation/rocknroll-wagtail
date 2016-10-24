from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Artist


def artist_list(request):
    artists = Artist.objects.all()

    paginator = Paginator(artists, 2)  # Show 2 contacts per page

    page = request.GET.get('page')
    try:
        artists = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        artists = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        artists = paginator.page(paginator.num_pages)

    return render(request, 'artist/artist_list.html', {
         'artists': artists,
    })
    # For more details on pagination
    # https://docs.djangoproject.com/en/1.10/topics/pagination/


def artist_genre_list(request, genre):
    artists = Artist.objects.all().filter(
        artist_genre_relationship__genres__slug=genre
        )

    return render(request, 'artist/artist_list.html', {
         'artists': artists,
    })


def artist_detail(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    articles = set(
        p.page for p in artist.artist_feature_page_relationship.select_related('page')
        .all() if p.page.live)
    albums = set(
        p.page for p
        in artist.artist_album_relationship.select_related('page')
        .all()
        )
    reviews = Artist.objects.all()
    # We use `page` because the parental key name is key on line 21 of
    # review/models.py
    #
    # We use `p` because I want to. You just need to use a variable that can be
    # passed through
    #
    # This works by getting pages into a list we can loop through on the template
    # It's `{classname}.{related_name}.select_related('page').all()`
    # Not entirely sure what `set` does other than to reverse order chronology
    #
    # Turn below in to useful thoughts... (what didn't work)
    #
    # artist.artist_album_relationship error = 'RelatedManager' object is not iterable
    #
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
         'review': reviews,
         'album': albums,
    })
