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
        related_name="genre_album_relationship"
    )
    panels = [
        FieldPanel('genres')
    ]


class AlbumArtistRelationship(Orderable, models.Model):
    page = ParentalKey(
        'Album',
        related_name='album_artist_relationship'
    )
    artist_name = models.ForeignKey(
        'artist.Artist',
        # app.class
        related_name="artist_album_relationship",
        help_text='The artist(s) who made this album'
    )
    panels = [
        SnippetChooserPanel('artist_name')
    ]


@register_snippet
class Album(ClusterableModel):

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('biography'),
    ]

    title = models.CharField("The album's name", blank=True, max_length=254)

    slug = models.SlugField(
        allow_unicode=True,
        max_length=255,
        help_text="The name of the page as it will appear in URLs e.g http://domain.com/blog/[my-slug]/",
    )

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

    @property
    def url(self):
        return '/albums/' + self.slug

    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        InlinePanel(
            'album_artist_relationship', label="Arist(s)", panels=None, min_num=1),
        ImageChooserPanel('image'),
        FieldPanel('release_date'),
        MultiFieldPanel(
            [
                InlinePanel(
                            'album_genre_relationship', label="Genre",
                            panels=None, min_num=1, max_num=1)
            ],
            heading="Genres",
            classname="collapsible"
        ),
        StreamFieldPanel('song_details'),
    ]

    def artists(self):
        artists = [
            n.artist_name for n in self.album_artist_relationship.all()
        ]
        return artists

    def genres(self):
        genres = [
            n.genres for n in self.album_genre_relationship.all()
        ]
        return genres

    def subgenres(self):
        subgenres = [
            n.subgenre for n in self.album_subgenre_relationship.all()
        ]
        return subgenres

    def __str__(self):
        string = (
            "Album: " + self.title +
            " by " +
            ','.join([str(self.artists())])
            )
        return string
        # This will return something like Album: 13 Songs by Fugazi
        # Need to get the result of the function call using artists(). Rather
        # than just artists. c/f http://stackoverflow.com/questions/31937532/python-django-query-error-cant-convert-method-object-to-str-implicitly
        # Then need to get the string out of the list
        # http://stackoverflow.com/questions/9165421/python-typeerror-cant-convert-list-object-to-str-implicitly

    @property
    def album_image(self):
        # fail silently if there is no profile pic or the rendition file can't
        # be found. Note @richbrennan worked out how to do this...
        try:
            return self.image.get_rendition('fill-400x400').img_tag()
        except:
            return ''

    def artist(obj):
        artist = ','.join([
            str(i.artist_name) for i in obj.album_artist_relationship.all()
            ])
        return artist
        # Note that we call `artist_name` because it's what we called the
        # ForeignKey on line 58 where we defined the relationship between
        # the album and artist in `AlbumArtistRelationship`

    artist.admin_order_field = 'album_artist_relationship__artist_name'

    def genre(obj):
        genre = ','.join([
                    str(n.genres) for n in obj.album_genre_relationship.all()
            ])
        return genre
        # Again note we call `genres` because it's what we called the fk

        genre.admin_order_field = 'album_genre_relationship__genre'

    class Meta:
        ordering = ['title']
        verbose_name = "Album"
        verbose_name_plural = "Albums"
