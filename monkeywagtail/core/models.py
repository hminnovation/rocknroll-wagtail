from django.db import models
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from monkeywagtail.core.blocks import ChildMenuBlock, ParentMenuBlock, MenuBlock


# MENUS
# We're creating a menu withing admin > settings > navigation menu
#
# This isn't standard Wagtail behaviour, which is to use the inbuilt `show-in-
# menu` flag on each page. If you wanted to use that you can implement it using
# templatetags. The best place to look for that is https://github.com/torchbox/
# wagtaildemo/blob/master/demo/templatetags/demo_tags.py to look directly at 
# code. There's also an excellent tutorial at http://www.tivix.com/blog/
# working-with-wagtail-menus/
#
# We can't use that standard page based paradigm (that uses TreeBeard) since we
# don't have a simple hierarchical tree relationship between content (e.g. 
# parent <-> child <-> grandchild) and are using generic models for author,
# album, artist and genre. 
#
# The menu here uses a StreamField block (based on two StructBlocks) that we de-
# fined in core/blocks.py. We pull that through as StreamField(MenuBlock())
# This works great if you just want a JSON output of the menu (since it's a
# StreamField object). 

# Note if you need a version that's based around fields then Jordi Joan has an
# awesome implementation that he blogged about at http://jordijoan.me/
# simple-orderable-menus-wagtail/


class Menus(ClusterableModel):
    title = models.CharField(max_length=255, null=False, blank=False, 
        verbose_name='Menu title')
    menu = StreamField(MenuBlock(), verbose_name="Menus", blank=True)

    panels = [
        FieldPanel('title'),
        StreamFieldPanel('menu'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Navigation menu"


# Related pages
class RelatedPage(Orderable, models.Model):
    page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, 
        on_delete=models.SET_NULL, related_name='+')

    class Meta:
        abstract = True
        ordering = ['sort_order']

    panels = [
        PageChooserPanel('page'),
    ]
