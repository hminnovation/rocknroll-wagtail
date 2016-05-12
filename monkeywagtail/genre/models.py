from django.db import models
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
# A snippet is a way to create non-hierarchy content on Wagtail (http://docs.wagtail.io/en/v1.4.3/topics/snippets.html)
# Wagtail 1.5 is likely to see these to either be deprecated, or at least used in very different ways
# They are currently quite limited against standard page models in how editors can access them. The easiest way
# to visualise that is probably to visit {whateverURLyouchose}/admin/snippets/author/author/
# Note: the properties and panels are defined in exactly the same way as on a page model
class Genre(models.Model):
    """
    You've gotta define a genre right
    """

    genre = models.CharField("The genre", max_length=254, help_text='The parent genre e.g. metal')

    sub_genre = StreamField([
        ('text', blocks.TextBlock(label='Sub-genre', help_text='Death metal, black metal etc.', icon="fa-music"))
    ])

    panels = [
        # The content panels are displaying the components of content we defined in the StandardPage class above
        # If you add something to the class and want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from wagtail.wagtailadmin.edit_handlers in
        # in the `From` statements at the top of the model
        FieldPanel('genre'),
        StreamFieldPanel('sub_genre')
    ]

    def __str__(self):              # __unicode__ on Python 2
        # We're returning the string that populates the snippets screen. Obvs whatever field you choose
        # will come through as plain text
        return self.genre
