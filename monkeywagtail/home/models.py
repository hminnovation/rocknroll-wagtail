from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel, MultiFieldPanel
from monkeywagtail.core.blocks import StandardBlock


class HomePage(Page):
    """
    The homepage for rock n roll wagtail
    @TODO explain what's going on... even if it is reasonably straight-forward

    """
    site_description_title = models.CharField(
        max_length=255,
        help_text='A title explaining this page.'
        )
    site_description = models.TextField(
        blank=True,
        help_text='A brief explanation of this page.'
        )

    advert_title = models.TextField(blank=True)
    advert_text = models.TextField(blank=True)
    advert_button = models.CharField(max_length=35, blank=True)
    advert_url = models.URLField("External link for advert", blank=True)

    # Page features
    featured_page_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Choose the most important feature page.',
        verbose_name='First featured page'
    )
    featured_page_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Choose the second most important featured page.',
        verbose_name='Second featured page'
    )
    featured_page_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Choose an important secondary page to feature.',
        verbose_name='Third featured page'
    )

    # Section features
    featured_section_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='A featured section showing the four most recently published items from that section.',
        verbose_name='Featured section one'
    )
    featured_section_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='A featured section showing the four most recently published items from that section.',
        verbose_name='Featured section two'
    )
    featured_section_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='A featured section showing the four most recently published items from that section.',
        verbose_name='Featured section three'
    )

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['children'] = Page.objects.live().in_menu().descendant_of(self)
        all_entries = Page.objects.all()
        return context

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('site_description_title'),
            FieldPanel('site_description'),
        ], heading="Description of the site"),
        MultiFieldPanel([
            FieldPanel('advert_text'),
            FieldPanel('advert_button'),
            FieldPanel('advert_url'),
        ], heading="Homepage advert"),
        MultiFieldPanel([
            PageChooserPanel('featured_page_1'),
            PageChooserPanel('featured_page_2'),
            PageChooserPanel('featured_page_3'),
            # PageChooserPanel('featured_page_3', 'events.EventIndexPage'),
        ], heading="Homepage features"),
        MultiFieldPanel([
            PageChooserPanel('featured_section_1'),
            PageChooserPanel('featured_section_2'),
            PageChooserPanel('featured_section_3'),
        ], heading="Homepage features")
    ]

    # Only let the root page be a parent
    parent_page_types = ['wagtailcore.Page']

    @property
    def children(self):
        children = self.get_children().live().in_menu().specific()
        return children

    class Meta:
        verbose_name = "Party on Wayne homepage"
