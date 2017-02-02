from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import (
        FieldPanel,
        InlinePanel,
        MultiFieldPanel,
        FieldRowPanel,
        TabbedInterface,
        ObjectList)
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey

COUNTRY_CHOICES = (
    ('austria', 'Austria'),
    ('belgium', 'Belgium'),
    ('denmark', 'Denmark'),
    ('finland', 'Finland'),
    ('france', 'France'),
    ('germany', 'Germany'),
    ('greece', 'Greece'),
    ('iceland', 'Iceland'),
    ('ireland', 'Ireland'),
    ('italy', 'Italy'),
    ('netherlands', 'Netherlands'),
    ('norway', 'Norway'),
    ('poland', 'Poland'),
    ('portugal', 'Portugal'),
    ('serbia', 'Serbia'),
    ('slovakia', 'Slovakia'),
    ('slovenia', 'Slovenia'),
    ('spain', 'Spain'),
    ('sweden', 'Sweden'),
    ('switzerland', 'Switzerland'),
    ('uk', 'United Kingdom (UK)')
)
# You could also consider https://github.com/SmileyChris/django-countries


class TourDates(Orderable):
    page = ParentalKey('TourPage', related_name='tourdates')
    date = models.DateField(blank=True, null=True)
    venue = models.CharField(max_length=255, help_text="Name of the venue")
    price = models.IntegerField(blank=True, null=True)
    door_open = models.TimeField(
        help_text="Time show starts", blank=True, null=True)
    city = models.CharField(
        max_length=255, help_text="City of the venue", blank=True, null=True)
    country = models.CharField(
        max_length=255, choices=COUNTRY_CHOICES
        )

    panels = [
        FieldRowPanel([
                FieldPanel('venue', classname="col6"),
                FieldPanel('date', classname="col6")
            ]),
        FieldRowPanel([
                FieldPanel('price', classname="col6"),
                FieldPanel('door_open', classname="col6")
            ]),
        FieldRowPanel([
                FieldPanel('city', classname="col6"),
                FieldPanel('country', classname="col6")
            ])
    ]


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
class TourAlbumRelationship(Orderable, models.Model):
    page = ParentalKey(
        'TourPage', related_name='tour_album_relationship'
    )
    albums = models.ForeignKey(
        'album.Album',
        related_name="album_tour_relationship"
    )
    panels = [
        SnippetChooserPanel('albums')
    ]


class TourArtistRelationship(Orderable, models.Model):
    page = ParentalKey(
        'TourPage',
        related_name='tour_artist_relationship'
    )
    artists = models.ForeignKey(
        'artist.Artist',
        # app.class
        related_name="artist_tour_relationship",
        help_text='The artist(s) who made this album'
    )
    panels = [
        SnippetChooserPanel('artists')
    ]


class TourPage(Page):

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('tour_description'),
    ]

    tour_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Album cover image'
    )

    tour_listing_introduction = models.TextField(
        "A listing introduction for the tour", blank=True, max_length=254
        )

    tour_description = RichTextField("A description for the tour")

    content_panels = Page.content_panels + [
        InlinePanel(
            'tour_artist_relationship', label="Arist(s)",
            panels=None, min_num=1),
        InlinePanel(
            'tour_album_relationship', label="Album(s)",
            panels=None, min_num=0),
        ImageChooserPanel('tour_image'),
        FieldPanel('tour_listing_introduction'),
        FieldPanel('tour_description'),
    ]

    tour_panels = [
        InlinePanel(
            'tourdates',
            label="Tour dates",
            help_text="Enter your tour dates",
            min_num=1
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Tour details", classname="content"),
        ObjectList(tour_panels, heading="Tour dates"),
        ObjectList(Page.promote_panels, heading="Promote"),
        ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
    ])

    # We iterate within the model over the artists, genres and subgenres
    # so they can be accessible to the template via a for loop
    def artists(self):
        artists = [
            n.artists for n in self.tour_artist_relationship.all()
        ]
        return artists

    def albums(self):
        albums = [
             n.albums for n in self.tour_album_relationship.all()
        ]

        return albums

    @property
    def album_image(self):
        # fail silently if there is no profile pic or the rendition file can't
        # be found. Note @richbrennan worked out how to do this...
        try:
            return self.image.get_rendition('fill-400x400').img_tag()
        except:
            return ''

    parent_page_types = [
        'tours.TourIndexPage'
        # app.model
    ]

    subpage_types = [
    ]


class TourIndexPage(Page):
    listing_introduction = models.TextField(
        help_text="Text to describe this section. Will appear on other pages "
        "that reference this feature section",
        blank=True
    )
    introduction = models.TextField(
        help_text="Text to describe this section. Will appear on the page",
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('listing_introduction'),
        FieldPanel('introduction'),
    ]

    parent_page_types = [
        'home.HomePage'
    ]

    # Defining what content type can sit under the parent
    subpage_types = [
        'TourPage'
    ]
