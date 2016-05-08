from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from monkeywagtail.core.blocks import StandardBlock


class HomePage(Page):
    """
    A standard page style can be used for a range of “content” pages
    on the site. Using StreamField it can allow for adaptable content
    """
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    introduction = models.TextField(blank=True)
    body = StreamField(StandardBlock(), blank=True)

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['children'] = Page.objects.live().in_menu().child_of(self)
        return context

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('introduction'),
        StreamFieldPanel('body')
    ]
