from django.shortcuts import render, get_object_or_404
from .models import GenreClass


def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'genre/genre_list.html', {
        'genres': genres,
    })


def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    return render(request, 'genre/genre_detail.html', {
        'genre': genre,
    })
