from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Album


class AlbumAdmin(ModelAdmin):
    model = Album
    menu_label = 'Albums'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-asterisk'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    list_display = ('album_artist_relationship', 'album_name', 'release_date',)
    list_filter = ('album_artist_relationship', 'album_name',  'release_date',)
    search_fields = ('album_artist_relationship', 'album_name', 'release_date',)


modeladmin_register(AlbumAdmin)
