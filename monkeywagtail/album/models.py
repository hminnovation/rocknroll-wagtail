from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from datetime import datetime


class AlbumSongs(models.Model):
    album_song = models.CharField("Song name", max_length=255, blank=True)
    album_song_length = models.TimeField("Song length", blank=True)

    panels = [
        FieldPanel('album_song'),
        FieldPanel('album_song_length')
    ]

    class Meta:
        abstract = True


class AlbumSongsRelationship(Orderable, AlbumSongs):
    album_songs = ParentalKey('album', related_name='album_songs_relationship')


class AlbumArtistRelationship(Orderable, models.Model):
    ArtistRelationship = ParentalKey(
        'Album',
        related_name='album_artist_relationship'
    )
    artist_name = models.ForeignKey(
        'artist.Artist',
        #app.class
        related_name="+",
        help_text='The artist(s) who made this album'
    )
    panels = [
        SnippetChooserPanel('artist_name')
    ]


@register_snippet
# A snippet is a way to create non-hierarchy content on Wagtail (http://docs.wagtail.io/en/v1.4.3/topics/snippets.html)
# Wagtail 1.5 is likely to see these to either be deprecated, or at least used in very different ways
# They are currently quite limited against standard page models in how editors can access them. The easiest way
# to visualise that is probably to visit {whateverURLyouchose}/admin/snippets/author/author/
# Note: the properties and panels are defined in exactly the same way as on a page model
# TODO: The author and artist snippets are very close to identical (single change that the title property is artist_name
# on one and author_name on the other)
class Album(ClusterableModel):
    """
    The album snippet gives a way to add albums to a site and create a one-way relationship with content
    """

    search_fields = Page.search_fields + (
        # Defining what fields the search catches
        index.SearchField('artist_name'),
        index.SearchField('biography'),
    )

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

    @property
    def album_songs_in_editor(self):
        album_songs_in_editor = [
            n.album_song for n in self.album_songs_relationship.all()
        ]
        return album_songs_in_editor

    @property
    def album_artist(self):
        album_artist = [
            n.album_artist for n in self.album_artist_relationship.all()
        ]
        return album_artist

    panels = [
        # The content panels are displaying the components of content we defined in the StandardPage class above
        # If you add something to the class and want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from wagtail.wagtailadmin.edit_handlers in
        # in the `From` statements at the top of the model
        FieldPanel('album_name'),
        InlinePanel('album_artist_relationship', label="Arist(s)", panels=None, min_num=1),
        ImageChooserPanel('image'),
        FieldPanel('release_date'),
        MultiFieldPanel(
            [
                InlinePanel('album_songs_relationship', label="Songs for this album", min_num=1),
            ],
            heading="Album songs",
            classname="collapsible"
        )
    ]

    #@property
    #def album_name(self):
    #    return self.album_name

    def __str__(self):              # __unicode__ on Python 2
        # We're returning the string that populates the snippets screen. Obvs whatever field you choose
        # will come through as plain text
        return self.album_name

    class Meta:
    # We need to clarify the meta class else we get a issubclass() arg 1 error (which I don't really
    # understand)
        ordering = ['album_name']
        verbose_name = "Album"
        verbose_name_plural = "Albums"

    def get_context(self, request):
           context = super(Album, self).get_context(request)
#
#        # Add extra variables and return the updated context
#        return context
