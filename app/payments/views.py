from django.conf import settings
from django.http import HttpResponse, JsonResponse
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

        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': item.stripe_price_id,
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=f'{domain_url}success',
                cancel_url=f'{domain_url}item/{item.pk}/'
            )
            return JsonResponse({'session_id': session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
