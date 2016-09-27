from django.db import models
from django.db.models import Count
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField
from modelcluster.fields import ParentalKey
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    InlinePanel,
    MultiFieldPanel)
from monkeywagtail.core.blocks import StandardBlock
from monkeywagtail.author.models import Author


class ArtistFeaturePageRelationship(Orderable, models.Model):
    # http://www.tivix.com/blog/working-wagtail-i-want-my-m2ms/
    # This is the start of defining the m2m. The related name is the 'magic'
    # that Wagtail hooks to. The model name (artist) within the app (artist) is
    # a terrible naming convention that you should avoid. It's 'class.model'
    page = ParentalKey(
        'FeatureContentPage', related_name='feature_page_artist_relationship'
    )
    artist = models.ForeignKey(
        'artist.artist',
        related_name='artist_feature_page_relationship'
        # If a related name is set here you can use it on relations
        # otherwise you use the lowercase model name with `_set` e.g.
        # artistfeaturepagerelationship_set
        # c/f https://docs.djangoproject.com/en/1.10/topics/db/queries/#following-relationships-backward
    )
    panels = [
        # We need this for the inlinepanel on the Feature Content Page to grab hold of
        FieldPanel('artist')
    ]


class AuthorFeaturePageRelationship(Orderable, models.Model):
    # We get to define another m2m for authors since a page can have many authors
    # and authors can obviously have many pages. You will see that the modelname
    # and appname are once again identical because I'm not very good at this game!
    page = ParentalKey(
        'FeatureContentPage', related_name='feature_page_author_relationship'
    )
    author = models.ForeignKey(
        'author.author',
        related_name="author_feature_page_relationship"
    )
    panels = [
        # We need this for the inlinepanel on the Feature Content Page to grab hold of
        FieldPanel('author')
    ]


class FeatureContentPage(Page):
    """
    This is a feature content page for all of your interviews, news etc.
    """

    # TODO This almost entirely duplicates StandardPage class. They should be referencing something
    # to reduce the duplication

    search_fields = Page.search_fields + [
        # Defining what fields the search catches
        index.SearchField('introduction'),
        index.SearchField('body'),
    ]

    date = models.DateField("Post date", help_text='blah')

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Image to be used where this feature content is listed'
    )

    # Note below that standard blocks use 'help_text' for supplementary text
    # rather than 'label' as with StreamField
    introduction = models.TextField(
        blank=True,
        help_text="Text to show at the top of the individual page")

    # Using CharField for little reason other than showing a different input
    # type Wagtail allows you to use any field type Django follows, so you can
    # use anything from
    # https://docs.djangoproject.com/en/1.9/ref/models/fields/#field-types
    listing_introduction = models.CharField(
        max_length=250,
        blank=True,
        help_text="Text shown on listing pages, if empty will show 'Introduction' field content")

    # Note below we're calling StreamField from another location. The
    # `StandardBlock` class is a shared asset across the site. It is defined in
    # core > blocks.py. It is just as 'correct' to define the StreamField
    # directly within the model, but this method aids consistency.
    body = StreamField(
        StandardBlock(),
        help_text="Blah blah blah",
        blank=True
        )

    content_panels = Page.content_panels + [
        # The content panels are displaying the components of content we defined
        # in the StandardPage class above. If you add something to the class and
        # want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at
        # http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from
        # wagtail.wagtailadmin.edit_handlers in the `From` statements at the top
        # of the model InlinePanel('artist_groups', label="Artist(s)"),
        # SnippetChooserPanel('artist'),
        FieldPanel('date'),
        MultiFieldPanel(
            [
                ImageChooserPanel('image'),
                FieldPanel('introduction'),
                FieldPanel('listing_introduction'),
            ],
            heading="Introduction and listing image",
            classname="collapsible"
        ),
        StreamFieldPanel('body'),
        InlinePanel('feature_page_artist_relationship', label="Artists"),
        InlinePanel(
            'feature_page_author_relationship',
            label="Authors",
            help_text='something'),
    ]

    @property
    def features_index(self):
        # I'm not convinced this is altogether necessary... but still we're
        # going from feature_content_page -> feature_index_page
        return self.get_ancestors().type(FeatureIndexPage).last()

    parent_page_types = [
        'feature_content_page.FeatureIndexPage'
        # app.model
    ]

    subpage_types = [
    ]

    # We're returning artists and authors to allow the template to grab the
    # related content. Note the fact we use the related name
    # `artist_feature_page_relationship` to grab them. In the template we'll use
    # a loop to grab them e.g. {% for artist in page.artists %}
    #
    # You don't need to place this at the end of the model, but conventionally
    # it makes sense to put it here
    def artists(self):
        artists = [
            n.artist for n in self.feature_page_artist_relationship.all()
        ]
        return artists

    def authors(self):
        authors = [
            n.author for n in self.feature_page_author_relationship.all()
        ]
        return authors


class FeatureIndexPage(Page):
    listing_introduction = models.TextField(
        help_text='Text to describe this section. Will appear on other pages that reference this feature section',
        blank=True
        )
    introduction = models.TextField(
        help_text='Text to describe this section. Will appear on the page',
        blank=True
        )
    body = StreamField(
        StandardBlock(),
        blank=True,
        help_text="No good reason to have this here, but in case there's a feature section I can't think of"
        )

    search_fields = Page.search_fields + [
        index.SearchField('listing_introduction'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('listing_introduction'),
        FieldPanel('introduction'),
        StreamFieldPanel('body')
    ]

    parent_page_types = [
        'home.HomePage'
    ]

    # Defining what content type can sit under the parent
    subpage_types = [
        'FeatureContentPage'
    ]

    @property
    def features(self):
        return FeatureContentPage.objects.live().descendant_of(self).order_by('-first_published_at')

    def artist_filter(self):
        artists = "abc"
        return artists

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.features, 2)  # Show 2 features per page
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        """
        Overriding the context to get more control over what we return.
        See the section `SEPARATED CONTEXT & PAGINATION` at the end of
        this .py file for details on how it works.
        """
        context = super(FeatureIndexPage, self).get_context(request)

        features = self.paginate(request, self.features)

        context['features'] = features

        return context

    # We use this property to allow the homepage to get the children of the
    # referenced index pages
    @property
    def children(self):
        return self.get_children().specific().live()

        # http://docs.wagtail.io/en/v1.2/topics/pages.html#customising-template-context

# SEPARATED CONTEXT & PAGINATION
#     def features(self):
#        return FeatureContentPage.objects.live().descendant_of(self).order_by('-first_published_at')
#        # We want to use `date` but think we need to define date within the filter?
#        #
#        # Previously self.get_children().specific().live().descendant_of(self).order_by('-first_published_at')
#        # Which I think is redundant since `get_children()` and `descendant_of(self)` are identical?
#
#    def paginate(self, request, *args):
#        page = request.GET.get('page')
#        paginator = Paginator(self.features, 2)  # Show 2 features per page
#        try:
#            pages = paginator.page(page)
#        except PageNotAnInteger:
#            pages = paginator.page(1)
#        except EmptyPage:
#            pages = paginator.page(paginator.num_pages)
#        return pages
#
#    def get_context(self, request):
#        """
#        Overriding the context to get more control over what we return.
#        """
#        context = super(FeatureIndexPage, self).get_context(request)
#
#        features = self.paginate(request, self.features)
#        # Right... I think I understand this
#        # the function `paginate` defines how the paginator should behave. We do
#        # this passing (I think) a local variable 'pages' through that is made
#        # available globally by the `paginate` function. On it's own it's inert.
#        # Calling `features = self.paginate will give you a sad white space where
#        # content should be. We need to make a request to the features function
#        # (where we define the queryset for the content we want returned) within
#        # paginate for anything to happen. We do this with
#        # features = self.paginate(request, self.features) e.g. give me all the
#        # features but wrap them with pagination.
#        #
#        # We need `self.` because we need to tell Python to go get them from
#        # FeatureIndexPage rather than from within the `get_context` function.
#        #
#        # Within paginate we add a third positional argument (that can be
#        # named whatever you want as far as I can tell, so have called it `*args` as
#        # that appears to be the convention) to enable `self.features` to be requested. Without it
#        # you'd get an error "paginate() takes 2 positional arguments but 3 were given"
#        #
#        #
#        # features_pagination = self.features(request)
#        # Without above we'll get an error local variable referenced before assignment.
#        # Unfortunately, with above we get the error
#        # 'PageQuerySet' object is not callable. Removing `(request)` removes the error
#
#        # pagination
#        # features_pagination = self.get_paginated(request, features_pagination)
#
#        context['features'] = features
#
#        return context
#
#
#
#
# MIXED CONTEXT & PAGINATION
# For reference below will work _and_ paginate
#
# The difficulty with this is that we're mixing pagination
# with context. It makes it quite difficult to follow the thread through
# as features and paginator have different attributes assigned before
# having features returned. It works fine, but isn't hugely extensible.
#
#    @property
#    def features(self):
#        return self.get_children().specific().live().descendant_of(self).order_by('-first_published_at')
#        # We want to use `date` but think we need to define date within the filter?
#
#    def get_context(self, request):
#        # http://docs.wagtail.io/en/v1.2/topics/pages.html#customising-template-context
#        # That convention can only be used on page models. Which is a pain.
#        page_number = request.GET.get('page')
#        paginator = Paginator(self.features, settings.DEFAULT_PER_PAGE)
#        try:
#            features = paginator.page(page_number)
#        except PageNotAnInteger:
#            features = paginator.page(1)
#        except EmptyPage:
#            features = paginator.page(paginator.num_pages)
#
#        context = super().get_context(request)
#        context.update(features=features)
#
#        return context
#
#
# AMENDED CONTEXT
# The absolute minimum required (if you want to override the context) is:
#
#    def get_context(self, request):
#        context = super(FeatureIndexPage, self).get_context(request)
#
#        # Add extra variables and return the updated context
#        context['features'] = FeatureContentPage.objects.live().descendant_of(self).order_by('-first_published_at')
#        return context
