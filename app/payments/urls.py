from django.urls import path

from . import views

urlpatterns = [
    path('', views.ItemListView.as_view(), name='items'),
    path(
        'buy/<int:pk>/',
        views.create_checkout_session,
        name='create_checkout_session'
    ),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item_details'),
]
