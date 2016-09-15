from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from monkeywagtail.core.blocks import SongStreamBlock
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from datetime import datetime


class GenreClassAlbumRelationship(Orderable, models.Model):
    page = ParentalKey(
        'Album', related_name='genre_album_relationship'
    )
    genre = models.ForeignKey(
        'genre.GenreClass',
        related_name="+"
    )
    panels = [
        SnippetChooserPanel('genre')
    ]


class SubGenreClassAlbumRelationship(Orderable, models.Model):
    page = ParentalKey(
        'Album', related_name='subgenre_album_relationship'
    )
    subgenre = models.ForeignKey(
        'genre.SubgenreClass',
        related_name="+"
    )
    panels = [
        # We need this for the inlinepanel on the Feature Content Page to grab hold of
        SnippetChooserPanel('subgenre')
    ]


class AlbumSongs(models.Model):
    # Candidate for deletion. Removed from album model panel.
    album_song = models.CharField("Song name", max_length=255, blank=True)
    album_song_length = models.TimeField("Song length", blank=True)

    panels = [
        FieldPanel('album_song'),
        FieldPanel('album_song_length')
    ]

    class Meta:
        abstract = True


class AlbumSongsRelationship(Orderable, AlbumSongs):
    # Candidate for deletion.  Removed from album model panel.
    album_songs = ParentalKey('album', related_name='album_songs_relationship')


class AlbumArtistRelationship(Orderable, models.Model):
    # Candidate for deletion.  Removed from album model panel.
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

    song_details = StreamField(SongStreamBlock(), verbose_name="Songs", blank=True)

    @property
    def album_songs_in_editor(self):
        album_songs_in_editor = [
            n.album_song for n in self.album_songs_relationship.all()
        ]
        return album_songs_in_editor

    @property
    def album_artist(self):
        album_artist = [
            n.artist_name for n in self.album_artist_relationship.all()
        ]
        return album_artist

    @property
    def genre(self):
        genres = [
            n.genre for n in self.genre_album_relationship.all()
        ]
        return genres

    @property
    def subgenres(self):
        subgenres = [
            n.subgenre for n in self.subgenre_album_relationship.all()
        ]
        return subgenres

    panels = [
        FieldPanel('album_name'),
        InlinePanel('album_artist_relationship', label="Arist(s)", panels=None, min_num=1),
        ImageChooserPanel('image'),
        FieldPanel('release_date'),
        MultiFieldPanel(
            [
                InlinePanel('genre_album_relationship', label="Genre", panels=None, min_num=1, max_num=1),
                InlinePanel('subgenre_album_relationship', label="sub-genres", panels=None, min_num=1),
            ],
            heading="Genres",
            classname="collapsible"
        ),
        StreamFieldPanel('song_details'),
        # MultiFieldPanel(
        #     [
        #         InlinePanel('album_songs_relationship', label="Songs for this album", min_num=1),
        #     ],
        #     heading="Album songs",
        #     classname="collapsible"
        # ),
    ]

    def __str__(self):
        return self.album_name

    def get_context(self, request):
        context = super(Album, self).get_context(request)
        return context

    def artist(obj):
        artist = ','.join([str(i) for i in obj.album_artist])
        return artist

    # artist.admin_order_field = 'album_artist_relationship'
    # artist.admin_order_field = 'album_artist_relationship__artist_name'

    class Meta:
        ordering = ['album_name']
        verbose_name = "Album"
        verbose_name_plural = "Albums"

    # @property
    # def album_songs_two(self):
    #    album_songs_two = AlbumSongs.objects.live()
    #    return album_songs_two

    # Then on that same album model perhaps define the admin_order_field as:


# That should allow you to add artist to your AlbumAdmin list_display + list_filter (+ search_fields) fields.
        # get_author.short_description = 'Author'
        # get_author.admin_order_field = 'book__author'

#    @property
#    def sections(self):
#        sections = []
#        categories = PersonCategory.objects.all()
#        for category in categories:
#            # Get people for category
#            people = self.people.filter(person_category_relationship__category__pk=category.pk)
#            if people:
#                sections.append({
#                    "category": category,
#                    "people": people
#                })
#        return sections


#
#        # Add extra variables and return the updated context
#        return context
#
class AlbumIndexPage(Page):
    parent_page_types = [
        'home.HomePage'
    ]

    # Defining what content type can sit under the parent
    subpage_types = [
    ]

# Index page context to return content
# This works, but doens't paginate
    def get_context(self, request):
        context = super(Album, self).get_context(request)
        context['Album'] = Album.objects.live().order_by('-date')
        return context
