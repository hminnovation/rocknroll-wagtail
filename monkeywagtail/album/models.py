from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (
        FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel)
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from monkeywagtail.core.blocks import SongStreamBlock
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


# Many-to-many relationships
# The first three models in this document define many-to-many relationships
# with other models across the project.
#
# We create them by defining a ParentalKey, which in this case is 'Album' and
# a ForeignKey, which is different for each relationship.
#
# The key to the puzzle is the related_name within the ParentalKey. This allows
# us to get to the information we need. There's more documentation in relation
# to how this is working at the end of this document.
class GenreClassAlbumRelationship(Orderable, models.Model):
    page = ParentalKey(
        'Album', related_name='album_genre_relationship'
    )
    genres = models.ForeignKey(
        'genre.GenreClass',
        related_name="+"
    )
    panels = [
        FieldPanel('genres')
    ]


class SubGenreClassAlbumRelationship(Orderable, models.Model):
    page = ParentalKey(
        'Album', related_name='album_subgenre_relationship'
    )
    subgenre = models.ForeignKey(
        'genre.SubgenreClass',
        related_name="+"
    )
    panels = [
        # We need this for the inlinepanel on the Feature Content Page to grab
        # hold of
        FieldPanel('subgenre')
    ]


class AlbumArtistRelationship(Orderable, models.Model):
    ArtistRelationship = ParentalKey(
        'Album',
        related_name='album_artist_relationship'
    )
    artist_name = models.ForeignKey(
        'artist.Artist',
        # app.class
        related_name="+",
        help_text='The artist(s) who made this album'
    )
    panels = [
        SnippetChooserPanel('artist_name')
    ]


@register_snippet
class Album(ClusterableModel):

    search_fields = Page.search_fields + [
        index.SearchField('album_name'),
        index.SearchField('biography'),
    ]

    album_name = models.CharField("The album's name", blank=True, max_length=254)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Album cover image'
    )

    release_date = models.DateField()

    song_details = StreamField(
        SongStreamBlock(), verbose_name="Songs", blank=True)

    panels = [
        FieldPanel('album_name'),
        InlinePanel(
            'album_artist_relationship', label="Arist(s)", panels=None, min_num=1),
        ImageChooserPanel('image'),
        FieldPanel('release_date'),
        MultiFieldPanel(
            [
                InlinePanel(
                            'album_genre_relationship', label="Genre",
                            panels=None, min_num=1, max_num=1),
                InlinePanel(
                            'album_subgenre_relationship', label="sub-genres",
                            panels=None, min_num=1),
            ],
            heading="Genres",
            classname="collapsible"
        ),
        StreamFieldPanel('song_details'),
    ]

    def __str__(self):
        return self.album_name

    def get_context(self, request):
        context = super(Album, self).get_context(request)
        return context

    def artist(obj):
        artist = ','.join([str(i) for i in obj.album_artist])
        return artist

    artist.admin_order_field = 'album_artist_relationship__artist_name'

    def genre(obj):
        genre = ','.join([
                    str(n.genres) for n in obj.album_genre_relationship.all()
                    # We need to call `genres` because it's what we called the fk
            ])
        return genre

        genre.admin_order_field = 'album_genre_relationship__genre'

    class Meta:
        ordering = ['album_name']
        verbose_name = "Album"
        verbose_name_plural = "Albums"

# Missing index page?
# -------------------
# Normally, in Wagtail, if one were to use a generic ClusterableModel as `Album`
# is you'd use a page model (e.g. `AlbumIndexPage(Page)`) to return the context.
# As a full example if you wanted to experiment with it would be
#
# class AlbumIndexPage(Page):
#     parent_page_types = [
#         'home.HomePage'
#     ]
#
#     # Defining what content type can sit under the parent
#     subpage_types = [
#     ]
#
#     def get_context(self, request):
#         context = super(Album, self).get_context(request)
#         context['Album'] = Album.objects.live().order_by('-date')
#         return context
#
# We're taking a Django approach with this app though and using views.py and
# urls.py where we're using a ListView and a DetailView. For more info on that
# have a look in album/views.py
#
#
# Many-to-many relationships (cont...)
# ------------------------------------
# @TODO write the docs on this :)
