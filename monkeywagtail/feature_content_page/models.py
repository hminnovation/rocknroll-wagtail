from django.db import models
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField
#from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from monkeywagtail.core.blocks import StandardBlock
from monkeywagtail.author.models import Author
#from wagtail.wagtailsnippets.models import register_snippet


class ArtistFeaturePageRelationship(Orderable, models.Model):
    # http://www.tivix.com/blog/working-wagtail-i-want-my-m2ms/
    # This is the start of defining the m2m. The related name is the 'magic' that Wagtail
    # hooks to. The model name (artist) within the app (artist) is a terrible naming convention
    # that you should avoid. It's 'class.model'
    page = ParentalKey(
        'FeatureContentPage', related_name='artist_feature_page_relationship'
    )
    artist = models.ForeignKey(
        'artist.artist',
        related_name="+"
    )
    panels = [
        # We need this for the inlinepanel on the Feature Content Page to grab hold of
        FieldPanel('artist')
    ]

class AuthorFeaturePageRelationship(Orderable, models.Model):
    # We get to define another m2m for authors since a page can have many authors
    # and authors can obviously have many pages. You will see that the modelname and appname
    # are once again identical because I'm not very good at this game!
    page = ParentalKey(
        'FeatureContentPage', related_name='author_feature_page_relationship'
    )
    author = models.ForeignKey(
        'author.author',
        related_name="+"
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

    search_fields = Page.search_fields + (
        # Defining what fields the search catches
        index.SearchField('introduction'),
        index.SearchField('body'),
    )

    publication_date = models.DateField("Post date", help_text='blah')

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Image to be used where this feature content is listed'
    )

    # Note below that standard blocks use 'help_text' for supplementary text rather than 'label' as with StreamField
    introduction = models.TextField(blank=True, help_text="Text to show at the top of the individual page")

    # Using CharField for little reason other than showing a different input type
    # Wagtail allows you to use any field type Django follows, so you can use anything from
    # https://docs.djangoproject.com/en/1.9/ref/models/fields/#field-types
    listing_introduction = models.CharField(max_length=250, blank=True, help_text="Text shown on listing pages, if empty will show 'Introduction' field content")

    # Note below we're calling StreamField from another location. The `StandardBlock` class is a shared
    # asset across the site. It is defined in core > blocks.py. It is just as 'correct' to define
    # the StreamField directly within the model, but this method aids consistency.
    body = StreamField(StandardBlock(), help_text="Blah blah blah", blank=True)

    @property
    # We're returning artists for the FeatureContentPage class. Note the fact we're
    # using `artist_feature_page_relationship` to grab them
    def artists(self):
        artists = [
            n.artist for n in self.artist_feature_page_relationship.all()
        ]
        return artists

    @property
    # Now the authors get pulled in
    def authors(self):
        authors = [
            n.author for n in self.author_feature_page_relationship.all()
        ]
        return authors

    content_panels = Page.content_panels + [
        # The content panels are displaying the components of content we defined in the StandardPage class above
        # If you add something to the class and want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from wagtail.wagtailadmin.edit_handlers in
        # in the `From` statements at the top of the model
        # InlinePanel('artist_groups', label="Artist(s)"),
        # SnippetChooserPanel('artist'),
        FieldPanel('publication_date'),
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
        InlinePanel('artist_feature_page_relationship', label="Artists"),
        InlinePanel('author_feature_page_relationship', label="Authors", help_text='something'),
    ]

    @property
    def features_index(self):
        # I'm not convinced this is altogether necessary... but still we're going from feature_content_page -> feature_index_page
        return self.get_ancestors().type(FeaturesIndexPage).last()

class FeaturesIndexPage(Page):
    def get_context(self, request):
        context = super(FeaturesIndexPage, self).get_context(request)
        context['features'] = FeatureContentPage.objects.live().descendant_of(self)
        return context

    # Defining what content type can sit under the parent
    subpage_types = ['FeatureContentPage']
