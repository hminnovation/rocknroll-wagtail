from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
# from wagtail.wagtaildocs.blocks import DocumentChooserBlock
# from wagtail.wagtailembeds.blocks import EmbedBlock
from django.utils.encoding import force_text
from django.utils.html import format_html_join, mark_safe
# from wagtailblocks_cards.blocks import CardsBlock


# class CardBlock(blocks.StructBlock):
# @TODO decide if this actually needs to be here.
#    image = ImageChooserBlock(required=False)
#    title = blocks.CharBlock()
#    body = blocks.TextBlock()
#    cta_page = blocks.PageChooserBlock(required=False)


class SongStreamBlock(blocks.StreamBlock):
    # Title name. Time.
    SongBlock = blocks.StructBlock([
        ('album_song', blocks.CharBlock(blank=True, required=False, label='e.g. Waiting Room')),
        ('album_song_length', blocks.TimeBlock(blank=True, required=False)),
    ], title="Song", icon="fa-music", template="blocks/songstreamblock.html")


class StreamBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph.html"
    )
    header = blocks.CharBlock(
        classname="title",
        icon="fa-header",
        template="blocks/h3.html"
    )
    image = blocks.StructBlock([
        ('image', ImageChooserBlock()),
        ('caption', blocks.CharBlock(blank=True, required=False)),
        ('style', blocks.ChoiceBlock(choices=[
            ('', 'Select an image size'),
            ('full', 'Full-width'),
            ('half', 'Half-width')
        ], required=False))
    ], icon="image", template="blocks/image.html")
    blockquote = blocks.StructBlock([
        ('text', blocks.TextBlock()),
        ('attribute_name', blocks.CharBlock(blank=True, required=False, label='e.g. Guy Picciotto')),
        ('attribute_group', blocks.CharBlock(blank=True, required=False, label='e.g. Fugazi')),
    ], icon="openquote", template="blocks/blockquote.html")


class StandardBlock(blocks.StreamBlock):
    # This class was originally writted by Alex Gleason (@alexgleason)
    paragraph = blocks.RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph.html"
    )
    h1 = blocks.CharBlock(
        classname="title",
        icon="fa-header",
        template="blocks/h1.html"
    )
    h2 = blocks.CharBlock(
        classname="title",
        icon="fa-header",
        template="blocks/h2.html"
    )
    h3 = blocks.CharBlock(
        classname="title",
        icon="fa-header",
        template="blocks/h3.html"
    )
    h4 = blocks.CharBlock(
        classname="title",
        icon="fa-header",
        template="blocks/h4.html"
    )
    image = blocks.StructBlock([
        ('image', ImageChooserBlock()),
        ('caption', blocks.CharBlock(blank=True, required=False)),
        ('style', blocks.ChoiceBlock(choices=[
            ('', 'Select an image size'),
            ('full', 'Full-width'),
            ('half', 'Half-width')
        ], required=False))
    ], icon="image", template="blocks/image.html")
    blockquote = blocks.StructBlock([
        ('text', blocks.TextBlock()),
        ('attribute_name', blocks.CharBlock(blank=True, required=False, label='e.g. Guy Picciotto')),
        ('attribute_group', blocks.CharBlock(blank=True, required=False, label='e.g. Fugazi')),
    ], icon="openquote", template="blocks/blockquote.html")

#    def render_basic(self, value):
#        headings = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

#        blocks = []
#        for i, child in enumerate(value):
#            childtype = child.block_type
#            childtext = force_text(child)
#            try:
#                nextchildtype = value[i+1].block_type
#                if childtype in headings and nextchildtype in bgs:
#                    childtext = '<div class="match-bg">{0}</div>'.format(
#                        force_text(child))
#                    childtext = mark_safe(childtext)
#            except IndexError:
#                pass
#            blocks.append((childtext, childtype))

#        return format_html_join('\n', '{0}', blocks)
