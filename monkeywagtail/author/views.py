from django.shortcuts import render, get_object_or_404
from .models import Author


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author/author_list.html', {
        'authors': authors,
    })


def author_detail(request, slug):
    author = get_object_or_404(Author, slug=slug)
    return render(request, 'author/author_detail.html', {
        'author': author,
    })
