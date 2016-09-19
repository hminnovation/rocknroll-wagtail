from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import MainMenu, FooterMenu


class MenuAdmin(ModelAdmin):
    model = MainMenu
    menu_label = 'Main menu'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-bars'  # use font awesome if you want
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    # add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    list_display = ('title',)
    # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_filter = ()
    search_fields = ('title',)

class FooterAdmin(ModelAdmin):
    model = FooterMenu
    menu_label = 'Footer menu'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-bars'  # use font awesome if you want
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    # add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    list_display = ('title',)
    # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_filter = ()
    search_fields = ('title',)


class MenuAdminGroup(ModelAdminGroup):
    menu_label = 'Menus'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 600  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False
    items = (MenuAdmin, FooterAdmin)

# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(MenuAdminGroup)
