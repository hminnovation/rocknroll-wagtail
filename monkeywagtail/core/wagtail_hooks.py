from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import Menus


class MenuAdmin(ModelAdmin):
    model = Menus
    menu_label = 'Menus'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-bars'  # use font awesome if you want
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    list_display = ('title',)
    # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_filter = ()
    search_fields = ('title',)


modeladmin_register(MenuAdmin)
