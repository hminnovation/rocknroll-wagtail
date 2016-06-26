from django.db import models
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailsnippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


@register_snippet
class SubgenreClass(ClusterableModel):

    subgenre = models.CharField(max_length=255, help_text="Be as esoteric as you'd like")
    description = models.TextField(blank=True, help_text='A description of the sub-genre')

    panels = [
        FieldPanel('subgenre'),
        FieldPanel('description')
    ]

    def __str__(self):              # __unicode__ on Python 2
        # We're returning the string that populates the snippets screen. Obvs whatever field you choose
        # will come through as plain text
        return self.subgenre

    class Meta:
        verbose_name = "Subgenre"
        verbose_name_plural = "Subgenres"


## This, calls _all_ of the fields from the snippet above, but not the actual content    
## It's because we don't have the next
class SubGenreRelationship(Orderable, SubgenreClass):
        subgenre_in_editor = ParentalKey('GenreClass', related_name='sub_genre_relationship')


@register_snippet
# A snippet is a way to create non-hierarchy content on Wagtail (http://docs.wagtail.io/en/v1.4.3/topics/snippets.html)
# Wagtail 1.5 is likely to see these to either be deprecated, or at least used in very different ways
# They are currently quite limited against standard page models in how editors can access them. The easiest way
# to visualise that is probably to visit {whateverURLyouchose}/admin/snippets/author/author/
# Note: the properties and panels are defined in exactly the same way as on a page model
class GenreClass(ClusterableModel):
    """
    You've gotta define a genre right
    """

    genre = models.CharField("The genre", max_length=254, help_text='The genre. Something high level e.g. pop, metal, punk etc')
    description = RichTextField(blank=True, help_text='A description of the genre')
    panels = [
        # The content panels are displaying the components of content we defined in the StandardPage class above
        # If you add something to the class and want it to appear for the editor you have to define it here too
        # A full list of the panel types you can use is at http://docs.wagtail.io/en/latest/reference/pages/panels.html
        # If you add a different type of panel ensure you've imported it from wagtail.wagtailadmin.edit_handlers in
        # in the `From` statements at the top of the model
        FieldPanel('genre'),
        FieldPanel('description'),
        InlinePanel('sub_genre_relationship', label="Subgenre", help_text="Note: this subgenres will populate the sub-genre snippet", min_num=1)
    ]

    def __str__(self):              # __unicode__ on Python 2
        # We're returning the string that populates the snippets screen. Obvs whatever field you choose
        # will come through as plain text
        return self.genre

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"