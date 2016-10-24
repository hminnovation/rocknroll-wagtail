from django.db import models
from django.contrib import admin
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
# from taggit.models import TaggedItemBase
from monkeywagtail.genre.models import SubgenreClass


class GenreArtistRelationship(Orderable, models.Model):
    page = ParentalKey(
        'Artist', related_name='artist_genre_relationship'
    )
    genres = models.ForeignKey(
        'genre.GenreClass',
        related_name='genre_artist_relationship'
    )
    panels = [
        FieldPanel('genres')
    ]


@register_snippet
# A snippet is created by adding a `@snippet` decorator to a ClusterableModel.
#
# A snippet is a way to create non-hierarchy content on Wagtail
# (http://docs.wagtail.io/en/v1.4.3/topics/snippets.html)
# Since Wagtail 1.5 introduced ModelAdmin to core it's likely we'll see these
# used less as it's now much easier to use generic models than it was before.
#
# They are used throughout this project though to enable us to use the
# SnippetChooserPanels, which make the UI to select the relationships slightly
# nicer. Note, however, that we're mostly accessing them via ModelAdmin (have
# a look at wagtail_hooks.py to see how we're doing that) rather than via the
# snippets admin screen. ModelAdmin gives us _a lot_ more control over how to
# display them.
#
# Arguably you could use a page model for an artist and have an information
# architecture that looks like
#
# artist index page (page)
#   |
#   |__ Nirvana (page)
#         |
#         |__ Bleach (page)
#         |
#         |__ Nevermind (page)
#
# But this would cause us all sorts of difficulties where we have albums by
# multiple artists (e.g. split records or compilations) and would be useless if
# we ever wanted to extend the site beyond the paradigm of artist albums.
#
class Artist(ClusterableModel):
    """
    The artist snippet gives content fields to define an artist
    """

    title = models.CharField("The artist's name", max_length=254)

    slug = models.SlugField(
        allow_unicode=True,
        max_length=255,
        help_text="The name of the page as it will appear in URLs e.g http://domain.com/blog/[my-slug]/",
    )

    search_fields = Page.search_fields + [
        # Defining what fields the search catches
        index.SearchField('title'),
        index.SearchField('biography'),
    ]

    profile_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    # What's with the surprised guy '+'
    # Django and Wagtail can sometimes clash because of the reverse relation that
    # Django will create for a ForeignKey. There's a GitHub issue about it where
    # @Kaedroho and @timheap go in to some details about the issue
    # https://github.com/torchbox/wagtail/issues/503 In brief were a class
    # called 'profile_image' a ValueError would be raised
    #
    # Using `related_name='+'` breaks this reverse relation. Where we _do_ have
    # a reverse relation that we want to maintain it's important that you give
    # it a unique name
    # https://docs.djangoproject.com/en/dev/topics/db/models/#specifying-the-parent-link-field

    date_formed = models.DateField("Date the artist started", blank=True, null=True)

    # tags = ClusterTaggableManager(through=GenreTagRelationship, blank=True)

    # Note below that standard blocks use 'help_text' for supplementary text
    # rather than 'label' as with StreamField
    biography = RichTextField(
        blank=True, help_text="Short biography about the user")

    external_url = models.URLField(blank=True, null=True)

    @property
    def url(self):
        return '/artists/' + self.slug

    panels = [
        # The content panels are displaying the components of content we defined
        # in the StandardPage class above. If you add something to the class and
        # want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at
        # http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from
        # wagtail.wagtailadmin.edit_handlers in the `From` statements at the top
        # of the model
        FieldPanel('title'),
        FieldPanel('slug'),
        InlinePanel(
            'artist_genre_relationship',
            label="Genre",
            panels=None,
            min_num=1,
            max_num=1
        ),
        ImageChooserPanel('profile_image'),
        FieldPanel('biography'),
        FieldPanel('date_formed'),
        FieldPanel('external_url')
    ]

    def __str__(self):
        # We're returning the string that populates the snippets screen.
        # Note it returns a plain-text string. Reference the `artist_image`
        # below for returning a HTML rendition
        return self.title

    # CONTENT FOR TEMPLATE
    def genres(self):
        genres = [
            n.genres for n in self.artist_genre_relationship.all()
        ]
        return genres

    # MODEL ADMIN THINGS
    @property
    def age(self):
        if self.date_formed:
            today = date.today()
            delta = relativedelta(today, self.date_formed)
            return str(delta.years)

    @property
    def artist_image(self):
        # fail silently if there is no profile pic or the rendition file can't
        # be found. Note @richbrennan worked out how to do this...
        try:
            return self.profile_image.get_rendition('fill-50x50').img_tag()
        except:
            return ''
        # c/f https://docs.python.org/3/tutorial/errors.html
        # for try / except explanation

    def genre(obj):
        genre = ','.join([
                str(n.genres) for n in obj.artist_genre_relationship.all()
        ])
        return genre

        artist.admin_order_field = 'artist_genre_relationship__genres'

    def decade_formed(self):
        # We fail silently because date formed isn't mandatory
        try:
            return self.date_formed.strftime('%Y')[:3] + "0's"
        except:
            return 'No date given'
    decade_formed.short_description = 'Decade the artist began'
    # We're extending date_formed so that it's slightly easier to filter when
    # there's lots of artists. The default returned by date_formed would be
    # dd MM yyyy (e.g. 08 Oct 2016), which is a bit too granular
    #
    # That's unfortunately the easy part...
    #
    # If you want to filter on it too (which you might well do) I can't figure
    # it out :(

    # def decade_formed_filter(obj):
    #         date = obj.date_formed.strftime('%Y')[:3] + "0's"
    #         return date


# class decade_born_list_filter(admin.SimpleListFilter):
#         # Human-readable title which will be displayed in the
#         # right admin sidebar just above the filter options.
#         title = ('decade formed')
#
#     # Parameter for the filter that will be used in the URL query.
#         parameter_name = 'decade'
#
#         def lookups(self, request, model_admin):
#             """
#             Returns a list of tuples. The first element in each
#             tuple is the coded value for the option that will
#             appear in the URL query. The second element is the
#             human-readable name for the option that will appear
#             in the right sidebar.
#             """
#             return (
#                 ('80s', _('in the eighties')),
#                 ('90s', _('in the nineties')),
#                 ('2010s', _('in the 2010s')),
#             )
#
#         def queryset(self, request, queryset):
#             """
#             Returns the filtered queryset based on the value
#             provided in the query string and retrievable via
#             `self.value()`.
#             """
#             # Compare the requested value (either '80s' or '90s')
#             # to decide how to filter the queryset.
#             if self.value() == '80s':
#                 return queryset.filter(
#                     date_formed__gte=date(1980, 1, 1),
#                     date_formed__lte=date(1989, 12, 31))
#             if self.value() == '90s':
#                 return queryset.filter(
#                     date_formed__gte=date(1990, 1, 1),
#                     date_formed__lte=date(1999, 12, 31))
#             if self.value() == '2010s':
#                 return queryset.filter(
#                     date_formed__gte=date(2010, 1, 1),
#                     date_formed__lte=date(2019, 12, 31))
#
#
# class PersonAdmin(admin.ModelAdmin):
#     list_filter = (DecadeBornListFilter,)
