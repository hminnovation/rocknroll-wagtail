from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtailblocks_cards.blocks import CardsBlock
from wagtail.wagtailcore.blocks import (
    StructBlock,
    TextBlock,
    StreamBlock,
    RichTextBlock,
    CharBlock,
    TimeBlock,
    ChoiceBlock,
    PageChooserBlock
)
# Note, you could import _all_ the blocks by using `from wagtail.wagtailcore
# import blocks`. But it's a bad idea to import everything.


class SongStreamBlock(StreamBlock):
    # Title name. Time.
    SongBlock = StructBlock([
        ('album_song', CharBlock(
            blank=True, required=False, label='e.g. Waiting Room')),
        ('album_song_length', TimeBlock(blank=True, required=False)),
    ], title="Song", icon="fa-music", template="blocks/songstreamblock.html")


class SimplifiedBlock(StreamBlock):
    paragraph = RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph.html"
    )
    header = CharBlock(
        classname="title",
        icon="fa-header",
        template="blocks/h3.html"
    )
    image = StructBlock([
        ('image', ImageChooserBlock()),
        ('caption', CharBlock(blank=True, required=False)),
        ('style', ChoiceBlock(choices=[
            ('', 'Select an image size'),
            ('full', 'Full-width'),
            ('half', 'Half-width')
        ], required=False))
    ], icon="image", template="blocks/image.html")
    blockquote = StructBlock([
        ('text', TextBlock()),
        ('attribute_name', CharBlock(
            blank=True, required=False, label='e.g. Guy Picciotto')),
        ('attribute_group', CharBlock(
            blank=True, required=False, label='e.g. Fugazi')),
    ], icon="openquote", template="blocks/blockquote.html")
    embed = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        template="blocks/embed.html")


class StandardBlock(StreamBlock):
    # This class was originally writted by Alex Gleason (@alexgleason)
    paragraph = RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph.html"
    )
    h1 = CharBlock(
        classname="title",
        icon="fa-header",
        template="blocks/h1.html"
    )
    h2 = CharBlock(
        classname="title",
        icon="fa-header",
        template="blocks/h2.html"
    )
    h3 = CharBlock(
        classname="title",
        icon="fa-header",
        template="blocks/h3.html"
    )
    h4 = CharBlock(
        classname="title",
        icon="fa-header",
        template="blocks/h4.html"
    )
    image = StructBlock([
        ('image', ImageChooserBlock()),
        ('caption', CharBlock(blank=True, required=False)),
        ('style', ChoiceBlock(choices=[
            ('', 'Select an image size'),
            ('full', 'Full-width'),
            ('half', 'Half-width')
        ], required=False))
    ], icon="image", template="blocks/image.html")
    blockquote = StructBlock([
        ('text', TextBlock()),
        ('attribute_name', CharBlock(
            blank=True, required=False, label='e.g. Guy Picciotto')),
        ('attribute_group', CharBlock(
            blank=True, required=False, label='e.g. Fugazi')),
    ], icon="openquote", template="blocks/blockquote.html")


class ChildMenuBlock(StructBlock):
    link_text = CharBlock()
    internal_link = PageChooserBlock(
        blank=True, required=False, icon='fa-link')
    external_link = CharBlock(blank=True, required=False, icon='fa-link')
    # Above: Note we don't use a URLBlock because we need to use arbitrary
    # strings for internal links (e.g. /artists). This is probably a terrible
    # idea and there's likely a better solution, but this works...

    class Meta:
        template = 'blocks/menuitem_child.html'
# The above will give a StructBlock of content (e.g. the same fields will always
# be accessible to the user) to create child menu items


class ParentMenuBlock(StructBlock):
    parent_link_text = CharBlock()
    parent_internal_link = PageChooserBlock(
        blank=True, required=False, icon='fa-link')
    parent_external_link = CharBlock(blank=True, required=False, icon='fa-link')
    child_link = CardsBlock(ChildMenuBlock())

    class Meta:
        template = 'blocks/menuitem_parent.html'
        # help_text = 'abc' (just to note that you can have help_text here)

# The parent menu block is very similar to the child except that we have includ-
# ed the `ChildMenuBlock` within a `CardsBlock` wrapper. This uses the
# wagtailblocks_cards module to style them as a card in the UI to make it slight-
# ly easier to visual lots of child menu items at once.


class MenuBlock(StreamBlock):
    menu_item = ParentMenuBlock(icon='fa-link')
# We then wrap both the parent and child menu blocks within a StreamField block
