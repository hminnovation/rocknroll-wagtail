from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Author


def author_list(request):
    authors = Author.objects.all()

    paginator = Paginator(authors, 2)  # Show 2 contacts per page

    page = request.GET.get('page')
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        authors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        authors = paginator.page(paginator.num_pages)

    return render(request, 'author/author_list.html', {
         'authors': authors,
    })
    # For more details on pagination
    # https://docs.djangoproject.com/en/1.10/topics/pagination/


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
