from django.db import models
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
#from taggit.models import TaggedItemBase
from monkeywagtail.genre.models import SubgenreClass


class SubGenreClassRelationship(Orderable, models.Model):
    # http://www.tivix.com/blog/working-wagtail-i-want-my-m2ms/
    # This is the start of defining the m2m. The related name is the 'magic' that Wagtail
    # hooks to. The model name (artist) within the app (artist) is a terrible naming convention
    # that you should avoid. It's 'class.model'
    page = ParentalKey(
        'Artist', related_name='subgenre_artist_relationship'
    )
    subgenre = models.ForeignKey(
        'genre.SubgenreClass',
        related_name="+"
    )
    panels = [
        # We need this for the inlinepanel on the Feature Content Page to grab hold of
        SnippetChooserPanel('subgenre')
    ]

#class GenreTagRelationship(TaggedItemBase, GenreClass):
#    content_object = ParentalKey('artist.Artist', related_name='genres')


@register_snippet
# A snippet is a way to create non-hierarchy content on Wagtail (http://docs.wagtail.io/en/v1.4.3/topics/snippets.html)
# Wagtail 1.5 is likely to see these to either be deprecated, or at least used in very different ways
# They are currently quite limited against standard page models in how editors can access them. The easiest way
# to visualise that is probably to visit {whateverURLyouchose}/admin/snippets/author/author/
# Note: the properties and panels are defined in exactly the same way as on a page model
# TODO: The author and artist snippets are very close to identical (single change that the title property is artist_name
# on one and author_name on the other)
class Artist(ClusterableModel):
    """
    The author snippet gives a way to add authors to a site and create a one-way relationship with content
    """

    search_fields = Page.search_fields + (
        # Defining what fields the search catches
        index.SearchField('artist_name'),
        index.SearchField('biography'),
    )

    artist_name = models.CharField("The artist's name", blank=True, max_length=254)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    #tags = ClusterTaggableManager(through=GenreTagRelationship, blank=True)

    # Note below that standard blocks use 'help_text' for supplementary text rather than 'label' as with StreamField
    biography = RichTextField(blank=True, help_text="Short biography about the user")

    external_url = models.URLField(blank=True, null=True)

    @property
    # We're returning artists for the FeatureContentPage class. Note the fact we're
    # using `artist_feature_page_relationship` to grab them
    def subgenres(self):
        subgenres = [
            n.subgenre for n in self.subgenre_artist_relationship.all()
        ]
        return subgenres

    panels = [
        # The content panels are displaying the components of content we defined in the StandardPage class above
        # If you add something to the class and want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from wagtail.wagtailadmin.edit_handlers in
        # in the `From` statements at the top of the model
        FieldPanel('artist_name'),
        InlinePanel('subgenre_artist_relationship', label="Genres", panels=None, min_num=1),
        ImageChooserPanel('image'),
        FieldPanel('biography'),
        #FieldPanel('tags'),
        FieldPanel('external_url')
    ]

    def __str__(self):              # __unicode__ on Python 2
        # We're returning the string that populates the snippets screen. Note it returns as plain-text
        return self.artist_name

        class Meta:
        # We need to clarify the meta class else we get a issubclass() arg 1 error (which I don't really
        # understand)
            ordering = ['artist_name']
            verbose_name = "Artist"
            verbose_name_plural = "Artists"

    def get_context(self, request):
        context = super(Artist, self).get_context(request)

        # Add extra variables and return the updated context
        # context['artists'] = artist.objects.child_of(self).live()
        return context
