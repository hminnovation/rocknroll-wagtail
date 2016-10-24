from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import Artist


class ArtistAdmin(ModelAdmin):
    model = Artist
    menu_label = 'Artists'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-bolt'  # change as required
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    list_display = ('title', 'decade_formed', 'genre', 'artist_image')
    # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_filter = (
        'date_formed',
        'artist_genre_relationship__genres'
        )
    search_fields = ('title',)


modeladmin_register(ArtistAdmin)

# Note Andy Babic has now added exceptional documentation about ModelAdmin
# at http://docs.wagtail.io/en/latest/reference/contrib/modeladmin/index.html
