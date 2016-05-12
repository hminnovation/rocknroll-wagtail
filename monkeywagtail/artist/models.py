from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
# A snippet is a way to create non-hierarchy content on Wagtail (http://docs.wagtail.io/en/v1.4.3/topics/snippets.html)
# Wagtail 1.5 is likely to see these to either be deprecated, or at least used in very different ways
# They are currently quite limited against standard page models in how editors can access them. The easiest way
# to visualise that is probably to visit {whateverURLyouchose}/admin/snippets/author/author/
# Note: the properties and panels are defined in exactly the same way as on a page model
# TODO: The author and artist snippets are very close to identical (single change that the title property is artist_name
# on one and author_name on the other)
class Artist(models.Model):
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

    # Note below that standard blocks use 'help_text' for supplementary text rather than 'label' as with StreamField
    biography = RichTextField(blank=True, help_text="Short biography about the user")

    external_url = models.URLField(blank=True, null=True)

    panels = [
        # The content panels are displaying the components of content we defined in the StandardPage class above
        # If you add something to the class and want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from wagtail.wagtailadmin.edit_handlers in
        # in the `From` statements at the top of the model
        FieldPanel('artist_name'),
        ImageChooserPanel('image'),
        FieldPanel('biography'),
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
