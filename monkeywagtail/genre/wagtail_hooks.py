from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import GenreClass


class GenreAdmin(ModelAdmin):
    model = GenreClass
    menu_label = 'Genres'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-list-alt'  # change as required
    menu_order = 300
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    list_display = ('title', 'description')
    search_fields = ('title',)


# class GenreAdminGroup(ModelAdminGroup):
#     menu_label = 'Genres'
#     menu_icon = 'fa-music'  # change as required
#     menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
#     items = (GenreAdmin)


modeladmin_register(GenreAdmin)
