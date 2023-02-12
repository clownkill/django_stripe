from django.conf import settings
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
import stripe

from .models import Item


class ItemListView(ListView):
    model = Item
    context_object_name = 'items'


class ItemDetailView(DetailView):
    queryset = Item.objects.all()
    context_object_name = 'item'


def create_checkout_session(request, pk):
    if request.method == 'GET':
        item = get_object_or_404(Item, pk=pk)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': item.price,
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url='http://localhost:8000/',
            cancel_url=f'http://localhost:8000/item/{item.pk}/'
        )
        return redirect(session.url)
    return HttpResponse('error')

