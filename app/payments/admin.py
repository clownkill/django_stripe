from django.contrib import admin

from .models import Item, Tax, Discount, Order, OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'price',
    ]


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'amount',
    ]


@admin.register(Discount)
class Discount(admin.ModelAdmin):
    list_display = [
        'code',
        'amount',
        'valid_from',
        'valid_to',
        'active',
    ]
    list_editable = [
        'active',
    ]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = [
        'product',
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer',
        'created_at',
        'updated_at',
        'paid',
    ]
    list_filter = [
        'paid',
        'created_at',
        'updated_at',
    ]
    raw_id_fields = [
        'customer',
    ]
    inlines = [
        OrderItemInline,
    ]
