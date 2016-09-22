from django.utils.html import format_html, format_html_join
from django.conf import settings
from wagtail.wagtailcore import hooks

# Note this app was originally written by @alexgleason
# This app limits the Hallo RichTextField. In Wagtail
# 1.7 (or 1.8) this will hopefully cease to be relevant.
# For now though we need to reduce the amount of options
# in the RichTextField to encourage the editor to use
# Streamfield. c/f https://groups.google.com/forum/#!topic/wagtail/lHSRpSrYtN8
# for the original Google Group conversation on the subject.
#
# Arguably this could be placed within the `Core` but I wanted to make it clear
# that it was here, and enables it to be easily removed from the project by
# amending settings/base.py if you don't wish to limit hallo.


@hooks.register('insert_editor_js')
def hallo_inlineonly_plugin():
    js_files = [
        'js/hallo-plugins/hallo-inlineonly.js',
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('inlineonly');
        </script>
        """
    )
