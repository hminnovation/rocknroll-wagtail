from django.shortcuts import render, get_object_or_404
from .models import GenreClass


def genre_list(request):
    genres = GenreClass.objects.all()
    return render(request, 'genre/genre_list.html', {
        'genres': genres,
    })


def genre_detail(request, slug):
    genre = get_object_or_404(GenreClass, slug=slug)
    return render(request, 'genre/genre_detail.html', {
        'genre': genre,
    })


def subgenre_detail(request, slug, sub_genre_slug):
    genre = get_object_or_404(GenreClass, slug=slug, subgenre_url=sub_genre_slug)
    return render(request, 'genre/genre_detail.html', {
        'genre': genre,
    })

# This won't work in any way
# def subgenre_detail(request, slug, sub_genre_slug):
#    subgenre = get_object_or_404(SubgenreClass, subgenre_url=sub_genre_slug)
#    return render(request, 'genre/subgenre_detail.html', {
#        'subgenre': subgenre,
#    })
