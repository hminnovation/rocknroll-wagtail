from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from monkeywagtail.core.blocks import StandardBlock
from wagtail.wagtailsnippets.models import register_snippet


class ArtistFeaturePageRelationship(models.Model):
    # http://www.tivix.com/blog/working-wagtail-i-want-my-m2ms/
    # This is the start of defining the m2m. The related name is the bit of 'magic' that Wagtail
    # hooks to. The class (artist) within the model (artist) is a terrible naming convention
    # that I need to fix
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

    publication_date = models.DateField("Post date")

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
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
    body = StreamField(StandardBlock(), blank=True)

    @property
    # We're returning artists for the FeatureContentPage class. Note the fact we're
    # using `artist_feature_page_relationship` to grab them
    def artists(self):
        artists = [
            n.artist for n in self.artist_feature_page_relationship.all()
        ]
        return artists

    def get_context(self, request):
        # This is display view - I think - though I'm less show about what it's *actually* doing
        context = super(FeatureContentPage, self).get_context(request)
#        context['children'] = Page.objects.live().in_menu().child_of(self)
#        context['artist_groups'] = self.artist_groups_list
#        context['artist'] = self.artist
        return context

    content_panels = Page.content_panels + [
        # The content panels are displaying the components of content we defined in the StandardPage class above
        # If you add something to the class and want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from wagtail.wagtailadmin.edit_handlers in
        # in the `From` statements at the top of the model
        # InlinePanel('artist_groups', label="Artist(s)"),
        # SnippetChooserPanel('artist'),
        FieldPanel('publication_date'),
        ImageChooserPanel('image'),
        FieldPanel('introduction'),
        FieldPanel('listing_introduction'),
        StreamFieldPanel('body'),
        InlinePanel('artist_feature_page_relationship', label="Artists")
    ]