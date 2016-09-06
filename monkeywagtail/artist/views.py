from django.views.generic import DetailView
from django.utils import timezone
from artist.models import Artist


class ArtistDetailView(DetailView):

    queryset = Artist.objects.all()

    def get_object(self):
        # Call the superclass
        object = super(ArtistDetailView, self).get_object()
        # Record the last accessed date
        object.last_accessed = timezone.now()
        object.save()
        # Return the object
        return object
