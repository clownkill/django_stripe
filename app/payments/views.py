from django.views.generic import ListView

from .models import Item


class ItemListView(ListView):
    model = Item
    context_object_name = 'items'
