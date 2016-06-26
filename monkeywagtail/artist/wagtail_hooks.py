from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Artist


class ArtistAdmin(ModelAdmin):
    model = Artist
    menu_label = 'Artists'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-bolt'  # change as required
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    list_display = ('artist_name', 'external_url',)
    list_filter = ('artist_name',)
    search_fields = ('artist_name',)


modeladmin_register(ArtistAdmin)
