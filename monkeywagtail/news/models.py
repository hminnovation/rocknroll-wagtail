from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import (
        FieldPanel,
        InlinePanel,
        StreamFieldPanel,)
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from monkeywagtail.core.blocks import SimplifiedBlock
from modelcluster.fields import ParentalKey
from monkeywagtail.core.models import RelatedPage


# Related page relationship
class NewsRelatedPageRelationship(RelatedPage):
    source_page = ParentalKey(
        'news.NewsPage', related_name='related_pages')
# As you can see from the import the RelatedPage model is defined in the
# core app


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
class NewsAlbumRelationship(Orderable, models.Model):
    page = ParentalKey(
        'NewsPage', related_name='news_album_relationship'
    )
    albums = models.ForeignKey(
        'album.Album',
        related_name="album_news_relationship"
    )
    panels = [
        SnippetChooserPanel('albums')
    ]


class NewsArtistRelationship(Orderable, models.Model):
    page = ParentalKey(
        'NewsPage',
        related_name='news_artist_relationship'
    )
    artists = models.ForeignKey(
        'artist.Artist',
        # app.class
        related_name="artist_news_relationship",
        help_text='The artist(s) who made this album'
    )
    panels = [
        SnippetChooserPanel('artists')
    ]


class AuthorFeaturePageRelationship(Orderable, models.Model):
    # We get to define another m2m for authors since a page can have many authors
    # and authors can obviously have many pages. You will see that the modelname
    # and appname are once again identical because I'm not very good at this game!
    page = ParentalKey(
        'NewsPage', related_name='news_author_relationship'
    )
    author = models.ForeignKey(
        'author.author',
        related_name="author_news_relationship"
    )
    panels = [
        # We need this for the inlinepanel on the Feature Content Page to grab hold of
        SnippetChooserPanel('author')
    ]


class NewsPage(Page):

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('news_body'),
    ]

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='News image'
    )

    news_listing_introduction = models.TextField(
        "A listing introduction for the news item", blank=True, max_length=255
        )

    news_body = StreamField(
        SimplifiedBlock(),
        blank=True, verbose_name="And now... the news")

    content_panels = Page.content_panels + [
        InlinePanel(
            'news_artist_relationship', label="Arist(s)",
            panels=None, min_num=1),
        InlinePanel(
            'news_album_relationship', label="Album(s)",
            panels=None, min_num=0),
        InlinePanel(
            'news_author_relationship',
            label="Authors",
            help_text='Author for this news article'),
        ImageChooserPanel('image'),
        FieldPanel('news_listing_introduction'),
        StreamFieldPanel('news_body'),
        InlinePanel(
            'related_pages', label="Related pages",
            help_text="Other pages from across the site that relate to this "
            "news page")
    ]

    # We iterate within the model over the artists, genres and subgenres
    # so they can be accessible to the template via a for loop
    def artists(self):
        artists = [
            n.artists for n in self.news_artist_relationship.all()
        ]
        return artists

    def authors(self):
        authors = [
            n.author for n in self.news_author_relationship.all()
        ]
        return authors

    def albums(self):
        albums = [
             n.albums for n in self.news_album_relationship.all()
        ]

        return albums

    def relatedpages(self):
        relatedpages = [
            n.page for n in self.related_pages.all()
        ]
        return relatedpages

    @property
    def album_image(self):
        # fail silently if there is no profile pic or the rendition file can't
        # be found. Note @richbrennan worked out how to do this...
        try:
            return self.image.get_rendition('fill-400x400').img_tag()
        except:
            return ''

    parent_page_types = [
        'news.NewsIndexPage'
        # app.model
    ]

    subpage_types = [
    ]


class NewsIndexPage(Page):
    listing_introduction = models.TextField(
        help_text="Text to describe this section. Will appear on other pages "
        "that reference this news section",
        blank=True
    )
    introduction = models.TextField(
        help_text="Text to describe this section. Will appear on the index page",
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
        'NewsPage'
    ]
