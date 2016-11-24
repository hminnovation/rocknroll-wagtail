from django.db import models
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
# Look at artist/models.py, line 16 for info on snippets
class Author(models.Model):
    """
    The author snippet gives a way to relate authors to other content and create
    a range of relationships (e.g. one-to-one, one-to-many or many-to-many
    relationships) with content
    """

    search_fields = Page.search_fields + [
        # Defining what fields the search catches
        index.SearchField('title'),
        index.SearchField('biography'),
    ]

    title = models.CharField("The author's name", blank=True, max_length=254)

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
        related_name='+'
    )

    job_title = models.CharField(
        "The author's job title", blank=True, max_length=254,
        help_text="e.g. punk rock person"
        )

    # Note below that standard blocks use 'help_text' for supplementary text
    # rather than 'label' as with StreamField
    biography = RichTextField(
        blank=True, help_text="Short biography about the user")

    external_url = models.URLField(blank=True, null=True)

    @property
    def url(self):
        return '/authors/' + self.slug

    panels = [
        # The content panels are displaying the components of content we defined
        # in the StandardPage class above. If you add something to the class and
        # want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at
        # http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from
        # wagtail.wagtailadmin.edit_handlers in the `From` statements at the top
        # of the model
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('slug'),
            ],
            heading="Title"
        ),
        FieldPanel('job_title'),
        ImageChooserPanel('image'),
        FieldPanel('biography'),
        FieldPanel('external_url')
    ]

    def __str__(self):
        # We're returning the string that populates the snippets screen.
        # Note it returns a plain-text string. Reference the `artist_image`
        # below for returning a HTML rendition
        return self.title

    @property
    def image_listing(self):
        # fail silently if there is no profile pic or the rendition file can't
        # be found. Note @richbrennan worked out how to do this...
        try:
            return self.image.get_rendition('fill-150x150').img_tag()
        except:
            return ''

    @property
    def image_listing_small(self):
        # Needs to fail silently because image = null
        try:
            return self.image.get_rendition('fill-50x50').img_tag()
        except:
            return ''
        # @TODO Give a more attractive verbose name (e.g. image)
        # @TODO work out whether this is actually okay to do
        # It feels repetitive to have to define every image size

