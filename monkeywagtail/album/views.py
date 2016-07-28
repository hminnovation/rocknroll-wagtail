from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import (Album, AlbumIndexPage)


class IndexView(generic.ListView):
    template_name = 'album/album_index_page.html'
    context_object_name = 'latest_album_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Album.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Album
    template_name = 'album/album_page.html'


#class ResultsView(generic.DetailView):
#    model = Album
#    template_name = 'polls/results.html'


#from django.shortcuts import get_object_or_404, render
#from django.http import HttpResponseRedirect, HttpResponse
#from django.core.urlresolvers import reverse
#from django.shortcuts import render
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#
#from wagtail.wagtailcore.models import Page
#
#
#
#def album_index(request):
#    latest_albums_list = Album.objects.order_by('-pub_date')[:5]
#    context = {'latest_albums_list': latest_question_list}
#    return render(request, 'album/album_index_page.html', context)
#
#
#def album(request):
#    try:
#        album = Album.objects.get(pk=id)
#    except Album.DoesNotExist:
#        raise Http404("Album does not exist")
#    return render(request, 'album/album_page.html', {'album': album})