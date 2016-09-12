from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import Author


class AuthorAdmin(ModelAdmin):
    model = Author
    menu_label = 'Authors'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-github'  # use font awesome if you want
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    list_display = ('title', 'image_listing_small')
    # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_filter = ()
    search_fields = ('title',)


modeladmin_register(AuthorAdmin)
