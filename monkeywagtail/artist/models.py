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
# from taggit.models import TaggedItemBase
from monkeywagtail.genre.models import SubgenreClass


# Artist Album relationship
class ArtistAlbumRelationship(models.Model):
    AlbumRelationship = ParentalKey(
        'Artist',
        related_name='artist_album_relationship'
    )
    album = models.ForeignKey(
        'album.Album',
        # app.class
        related_name="+",
        help_text='The album being artisted'
    )
    panels = [
        SnippetChooserPanel('album')
    ]


@register_snippet
# A snippet is a way to create non-hierarchy content on Wagtail (http://docs.wagtail.io/en/v1.4.3/topics/snippets.html)
# Wagtail 1.5 is likely to see these to either be deprecated, or at least used in very different ways
# They are currently quite limited against standard page models in how editors can access them. The easiest way
# to visualise that is probably to visit {whateverURLyouchose}/admin/snippets/author/author/
# Note: the properties and panels are defined in exactly the same way as on a page model
# TODO: The author and artist snippets are very close to identical (single change that the title property is artist_name
# on one and author_name on the other)
#
# Note we could make our life easier here by not using a snippet. A page model would
# be easier to template and easier to filter. However, it we created a page model we
# wouldn't be able to have it under multiple genres...except we would
class Artist(ClusterableModel):
    """
    The author snippet gives a way to add authors to a site and create a one-way relationship with content
    """

    title = models.CharField("The artist's name", blank=True, max_length=254)

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

    date_formed = models.DateField("Date the artist started", blank=True, null=True)

    # tags = ClusterTaggableManager(through=GenreTagRelationship, blank=True)

    # Note below that standard blocks use 'help_text' for supplementary text rather than 'label' as with StreamField
    biography = RichTextField(blank=True, help_text="Short biography about the user")

    external_url = models.URLField(blank=True, null=True)

    @property
    def url(self):
        return '/artists/' + self.slug

    @property
    def albums(self):
        albums = [
            n.album for n in self.artist_album_relationship.all()
        ]
        return albums

    panels = [
        # The content panels are displaying the components of content we defined in the StandardPage class above
        # If you add something to the class and want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from wagtail.wagtailadmin.edit_handlers in
        # in the `From` statements at the top of the model
        FieldPanel('title'),
        FieldPanel('slug'),
        InlinePanel('artist_album_relationship', label="Album", panels=None),
        ImageChooserPanel('profile_image'),
        FieldPanel('biography'),
        FieldPanel('date_formed'),
        FieldPanel('external_url')
    ]

    def __str__(self):
        # We're returning the string that populates the snippets screen. Note it returns as plain-text
        return self.title

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

        class Meta:
            # We need to clarify the meta class else we get a issubclass() arg 1 error (which I don't really
            # understand)
            ordering = ['title']
            verbose_name = "Artist"
            verbose_name_plural = "Artists"

    def get_context(self, request):
        context = super(Artist, self).get_context(request)

        # Add extra variables and return the updated context
        # context['artists'] = artist.objects.child_of(self).live()
        return context
