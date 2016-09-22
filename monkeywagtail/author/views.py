from django.shortcuts import render, get_object_or_404
from .models import Author


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author/author_list.html', {
        'authors': authors,
    })


def author_detail(request, slug):
    author = get_object_or_404(Author, slug=slug)
    articles = set(
        p.page for p in author.author_feature_page_relationship.select_related('page').all() if p.page.live)
    reviews = set(
        p.page for p in author.author_review_relationship.select_related('page').all() if p.page.live)
    return render(request, 'author/author_detail.html', {
        'author': author,
        'article': articles,
        'review': reviews,
    })
