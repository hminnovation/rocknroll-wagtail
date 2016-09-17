from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Album


class AlbumAdmin(ModelAdmin):
    model = Album
    menu_label = 'Albums'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-asterisk'  # change to something font awesome-y as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # True will add your model to the Settings sub-menu

    list_display = ('artist', 'album_name', 'release_date',)
    list_filter = ('album_artist_relationship__artist_name', 
    	'genre_album_relationship__genres', 'release_date',)
    search_fields = ('artist', 'album_name', 'release_date',)


modeladmin_register(AlbumAdmin)

# You'll notice in list_display that we can use 'artist' whilst in list_filter
# we need to use 'album_artist_relationship__artist_name' to get the same info
# e.g. the name of the artist.
#
# This is to-do with what properties the two different options are set up to
# recognise.
#
# List_display
# Deeply over-simplifying it list_display needs a field on the model, an attribute 
# or a callable. Using `album_artist_relationship` would work to the extent that
# it wouldn't give an error but would display 'album.AlbumArtistRelationship.None'
#
# On the album model we defined a callable that accepted one parameter for the 
# model instance. In this case the name of the artist.
# list_display docs http://tinyurl.com/gm6o3co
#
# List_filter
# By contrast list_filter needs to be a specific field. In our case, because of
# the ClusterableModel we use the related name 'album_artist_relationship'
# Field names in list_filter can also span relations using the reverse 
# relationship (__) lookup. 'album_artist_relationship__artist_name' will let us
# get the artist's name, and as importantly, filter on it.
# list_filter docs are at http://tinyurl.com/z58c54n
# 