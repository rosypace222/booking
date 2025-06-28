from django.views.generic import ListView, DetailView
from .models import Space

class SpaceListView(ListView):
    model = Space
    template_name = 'core/space_list.html'
    context_object_name = 'spaces'
    paginate_by = 10

    def get_queryset(self):
        return Space.objects.filter(is_active=True).order_by('name')

class SpaceDetailView(DetailView):
    model = Space
    template_name = 'core/space_detail.html'
    context_object_name = 'space'
    slug_url_kwarg = 'slug'