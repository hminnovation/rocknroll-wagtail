from django.shortcuts import render, get_object_or_404
from .models import Album
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from django.views import generic


def album_list(request):
    albums = Album.objects.all()
    return render(request, 'album/album_list.html', {
         'albums': albums,
    })


def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug)
    reviews = set(
        p.page for p in album.album_review_relationship.select_related('page').all() if p.page.live)
    return render(request, 'album/album_detail.html', {
        'album': album,
        'review': reviews,
    })


# Below is an example of how you might want to articulate the view using Django's
# ListView and DetailView. I don't know enough as to why you'd use this instead
# of request functions
#
# class album_list(generic.ListView):
#     template_name = 'album/album_index_page.html'
#     context_object_name = 'latest_album_list'
#
#     def get_queryset(self):
#         """Return the last five published albums."""
#         return Album.objects.order_by('-pub_date')[:5]
#
#
# class album_detail(generic.DetailView):
#     model = Album
#     template_name = 'album/album_page.html'
