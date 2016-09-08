from django.shortcuts import render, get_object_or_404
from .models import Artist


def artist_list(request):
    artists = Artist.objects.all()
    return render(request, 'artist/artist_list.html', {
        'artists': artists,
    })


def artist_detail(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    return render(request, 'artist/artist_detail.html', {
        'artist': artist,
    })


# def get_artist_url(self):
#     return reverse("artists:index", kwargs={"pk": self.object.pk})
