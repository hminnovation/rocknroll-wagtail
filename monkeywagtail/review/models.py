import collections

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailsearch import index
# from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel, InlinePanel, TabbedInterface, ObjectList,
    MultiFieldPanel)
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey
from monkeywagtail.core.blocks import SimplifiedBlock
from monkeywagtail.core.models import RelatedPage

FilterObject = collections.namedtuple('FilterObject', 'id, name, slug, artist')

# Related page relationship
class ReviewRelatedPageRelationship(RelatedPage):
    source_page = ParentalKey(
        'review.ReviewPage', related_name='related_pages')


# Album
class ReviewAlbumRelationship(models.Model):
    page = ParentalKey(
        'ReviewPage',
        related_name='review_album_relationship'
    )
    album = models.ForeignKey(
        'album.Album',
        # app.class
        related_name="album_review_relationship",
        help_text='The album being reviewed'
    )
    panels = [
        SnippetChooserPanel('album')
    ]


# And the authors
class ReviewAuthorRelationship(models.Model):
    page = ParentalKey(
        'ReviewPage',
        related_name='review_author_relationship'
    )
    author = models.ForeignKey(
        'author.Author',
        # app.class
        related_name="author_review_relationship",
        help_text='The author who wrote this'
    )
    panels = [
        SnippetChooserPanel('author')
    ]


class ReviewPage(Page):
    """
    This is a page for an album review
    """

    search_fields = Page.search_fields + [
        # Defining what fields the search catches
        index.SearchField('introduction'),
        index.SearchField('body'),
    ]

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Image to be used where this review is listed'
    )

    # Note the integerfield can't just have a max_value and min_value assigned,
    # but needs to import the validators from django. It frankly feels silly to
    # do that, but that's what you have to do!
    rating = models.IntegerField("Album rating", validators=[
        MinValueValidator(0), MaxValueValidator(5)],
        help_text="Your rating needs to be between 0 - 5")

    # Note below that standard blocks use 'help_text' for supplementary text
    # rather than 'label' as with StreamField
    introduction = models.TextField(
        blank=True, help_text="Text to show at the review page")

    # Using CharField for little reason other than showing a different input type
    # Wagtail allows you to use any field type Django follows, so you can use
    # anything from
    # https://docs.djangoproject.com/en/1.9/ref/models/fields/#field-types
    listing_introduction = models.CharField(
        max_length=250, blank=True,
        help_text="Text shown on review, and other, listing pages, if empty will show 'Introduction' field content"
        )

    # Note below we're calling StreamField from another location. The
    # `SimplifiedBlock` class is a shared asset across the site. It is defined
    # in core > blocks.py. It is just as 'correct' to define the StreamField
    # directly within the model, but this method aids consistency.
    body = StreamField(
        SimplifiedBlock(),
        blank=True, verbose_name="Review body")

    def get_context(self, request):
        # @TODO. Work out if we actually do need/want to return this?
        # We're not allowing reviews to be nested under reviews so feels
        # unnecessary
        context = super(ReviewPage, self).get_context(request)
        context['children'] = Page.objects.live().in_menu().child_of(self)
        return context

    content_panels = Page.content_panels + [
        # The content panels are displaying the components of content we defined
        # in the ReviewPage class above. If you add something to the class and
        # want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at
        # http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from
        # wagtail.wagtailadmin.edit_handlers in the `From` statements at the top
        # of the model
        InlinePanel('review_album_relationship', label="Album", min_num=1,
                    max_num=1),
        InlinePanel(
            'related_pages', label="Related pages",
            help_text="Other pages from across the site that relate to this review")
    ]

    review_panels = [
        FieldPanel('rating'),
        MultiFieldPanel(
            [
                FieldPanel('introduction'),
                FieldPanel('listing_introduction'),
            ],
            heading="Introduction",
            classname="collapsible"
        ),
        StreamFieldPanel('body'),
        InlinePanel('review_author_relationship', label="Author", min_num=1),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Album details", classname="content"),
        ObjectList(review_panels, heading="Review"),
        ObjectList(Page.promote_panels, heading="Promote"),
        ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
    ])

    subpage_types = []

    parent_page_types = [
        'ReviewIndexPage'
    ]

    @property
    def artists(self):
        artists = [
            n.artist for n in self.review_artist_relationship.all()
        ]
        return artists

    @property
    def albums(self):
        albums = [
            n.album for n in self.review_album_relationship.all()
        ]
        return albums

    @property
    def authors(self):
        authors = [
            n.author for n in self.review_author_relationship.all()
        ]
        return authors


# class ReviewFeatureIndexPage(Page):
#     content_panels = Page.content_panels + []
#
#     class Meta:
#         verbose_name = "Reviews for albums with 4+ reviews"
#
#     subpage_types = []
#
#     parent_page_types = [
#         'ReviewIndexPage'
#     ]
#
#     def get_context(self, request):
#         context = super(ReviewFeatureIndexPage, self).get_context(request)
#
#         reviews = ReviewPage.objects.live().filter(rating__gte=4).order_by('-first_published_at')
#
#         context['reviews'] = reviews
#         return context


class ReviewIndexPage(Page):
    listing_introduction = models.TextField(
        help_text='Text to describe this section. Will appear on other pages that reference this feature section',
        blank=True)
    introduction = models.TextField(
        help_text='Text to describe this section. Will appear on the page',
        blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('listing_introduction'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('listing_introduction'),
        FieldPanel('introduction')
    ]

    parent_page_types = [
        'home.HomePage'
    ]

    # Defining what content type can sit under the parent
    subpage_types = [
        'ReviewPage'
    ]

    def paginate(self, request, objects):
        page = request.GET.get('page')
        paginator = Paginator(objects, 10)  # Show 20 objects per page
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def artists(self):
        """
        Return a list of artists from reviews that have a relationship defined
        with an album and are living beneath this page.
        """
        artists = set()
        # Don't duplicate
        for review_page in ReviewPage.objects.live().descendant_of(self):
            import pdb; pdb.set_trace()
            review_page_albums = [
                n.album for n in review_page.review_album_relationship.all()
                ]
            for album in review_page_albums:
                artists = [
                    n.artist_name for n in album.album_artist_relationship.all()
                ]
            # review_page = [
            #     d.albums for d in ReviewPage.objects.live().descendant_of(self)
            # ]
        # albums = [
        #         d.album for d in
        #         review_page.title.all()
        #     ]
        # artists = [
        #         d.artist_name for d in
        #         albums.album_artist_relationship.all()
        #     ]

        # return sorted(artists, key=lambda d: d.artists)
        return sorted(artists)

    def get_filtered_review_pages(self, request={}):
        # useful primer about defining python functions
        # https://www.tutorialspoint.com/python/python_functions.htm

        reviews = ReviewPage.objects.live().descendant_of(self).order_by('-first_published_at')
        # This is the default context for the reviews index page

        is_filtering = False
        # By default we return an unfiltered list

        request_filters = {}
        for k, v in request.GET.items():
            request_filters[k] = (v)

        # filter on rating
        rating = request_filters.get('rating', '')
        if rating:
            is_filtering = True
            reviews = reviews.filter(
                rating__gte=rating
            )

        # filter on first letter of review page album
        artist_name = request_filters.get('artist_name', '')
        if artist_name:
            is_filtering = True
            reviews = reviews.filter(
                review_album_relationship__album__album_artist_relationship__artist_name__title__istartswith=artist_name
            )

        # filter by genre
        genre = request_filters.get('genre', '')
        if genre:
            is_filtering = True
            reviews = reviews.filter(
                review_album_relationship__album__album_genre_relationship__genres__slug=genre
            )

        sort_by = request_filters.get('sort_by', 'modified')
        if sort_by == 'rating-asc':
            reviews = reviews.order_by('-rating', '-first_published_at')
        if sort_by == 'rating-desc':
            reviews = reviews.order_by('rating', '-first_published_at')
            # We need to give the date to ensure that there's ordering consistency
            # within ratings (e.g. that all reviews marked 5 are ordered chronologically)
            # Django doesn't take an opinion on how to order lists so will randomly
            # order if not set. "If a query doesn’t have an ordering specified,
            # results are returned from the database in an unspecified order. "
            # https://docs.djangoproject.com/en/1.10/ref/models/querysets/#order-by

        # Defining the filter
        filters = {
            'rating': rating,
            'artist_name': artist_name,
            'genre': genre,
            'sort_by': sort_by,
        }

        return reviews, filters, is_filtering

# Index page context to return content
# This works, but doens't paginate
    def get_context(self, request):
        # returning a dictionary of content
        context = super(ReviewIndexPage, self).get_context(request)

        # Running that dict() through my page models get_filtered_review_pages function
        reviews, filters, is_filtering = self.get_filtered_review_pages(request)

        # Pagination. Has to be after reviews is defined
        reviews = self.paginate(request, reviews)

        context['reviews'] = reviews
        context['filters'] = filters
        context['is_filtering'] = is_filtering
        # context['reviews'] = ReviewPage.objects.descendant_of(self).live().order_by('-first_published_at')
        return context

# Below is how we get children of reviews (i.e a review) on to the homepage
    @property
    def children(self):
        return self.get_children().specific().live()

# Optional arguments
# context
#
# A dictionary of values to add to the template context. By default, this is an
# empty dictionary. If a value in the dictionary is callable, the view will call
# it just before rendering the template.
# So :
#
# def all_contacts(request):
#     context = dict()
#     context['contacts'] = Contact.objects.all()
#     context['otherStuffProcessedByTheTemplate'] = …
#     # etc…
#
#     return render(request, 'about/all.html', context)
