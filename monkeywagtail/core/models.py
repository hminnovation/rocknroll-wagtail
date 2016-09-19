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


# We're cheating here. Slightly. Wagtail comes with the built-in functionality of `show-in-menu`
# You can access that via using templatetags. The best place to look for that is https://github.com/torchbox/wagtaildemo/blob/master/demo/templatetags/demo_tags.py
# if you want to look directly or code, or the very excellent http://www.tivix.com/blog/working-with-wagtail-menus/
# if you want, you know, some _actual_ documentation.
#
# We're cheating because the templatetag uses TreeBeard, which requires a simple hierarchical tree relationship
# between content (e.g. parent -> child -> grandchild), which we don't have on this site. We can hack our way around
# it within the templatetag (by defining different contexts) but it's a lot easier to do it via a snippet.
#
# This is based off of http://jordijoan.me/simple-orderable-menus-wagtail/ by Jordi Joan

class MenuItems(models.Model):
    """
    Represents a link to an external page, a document or a Wagtail page
    """
    link_external = models.URLField(
        "External link",
        blank=True,
        null=True,
        help_text='Set an external link if you want the link to point somewhere outside the CMS.'
    )
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose an existing page if you want the link to point somewhere inside the CMS.'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose an existing document if you want the link to open a document.'
    )

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document')
    ]

    class Meta:
        abstract = True


class MenuMenuItemRelationship(Orderable, MenuItems):
    links_in_menu = ParentalKey('core.Menu', related_name='menu_items')


# class MenuManager(models.Manager):
#    def get_by_natural_key(self, name):
#        return self.get(menu_name=name)


@register_snippet
class Menu(ClusterableModel):
    # objects = MenuManager()
    menu_name = models.CharField(max_length=255, null=False, blank=False)

    @property
    def menu_items_template(self):
        menu_items_template = self.menu_items.all()
        return menu_items_template

    def __str__(self):              # __unicode__ on Python 2
        return self.menu_name

    class Meta:
        verbose_name = "Navigation menu"

Menu.panels = [
    FieldPanel('menu_name', classname='full title'),
    InlinePanel('menu_items', label="Menu Items", min_num=1, help_text='Set the menu items for the current menu.')
]


class Menus(ClusterableModel):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Menu title')
    menu = StreamField(MenuBlock(), verbose_name="Menus", blank=True)

    panels = [
        FieldPanel('title'),
        StreamFieldPanel('menu'),
    ]

# Related pages
class RelatedPage(Orderable, models.Model):
    page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        abstract = True
        ordering = ['sort_order']

    panels = [
        PageChooserPanel('page'),
    ]
