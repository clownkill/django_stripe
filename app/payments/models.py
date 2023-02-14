from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
import stripe


class Item(models.Model):

    name = models.CharField('Название', max_length=150, db_index=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    stripe_product_id = models.CharField(max_length=150, blank=True)
    stripe_price_id = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Tax(models.Model):

    name = models.CharField('Название налога', max_length=150)
    amount = models.PositiveSmallIntegerField(
        'Величина налога',
        validators=[MaxValueValidator(100)],
    )

    class Meta:
        ordering = ('amount',)
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

    def __str__(self):
        return self.name


class Discount(models.Model):

    code = models.CharField(
        'Купон',
        max_length=50,
        unique=True,
    )
    valid_from = models.DateTimeField('Действителен с')
    valid_to = models.DateTimeField('Действителен по')
    amount = models.PositiveSmallIntegerField(
        'Величина скидки',
        validators=[MaxValueValidator(100)]
    )
    active = models.BooleanField('Активный?')

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.code


class Order(models.Model):

    customer = models.ForeignKey(
        User,
        verbose_name='Покупатель',
        related_name='orders',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    tax = models.ForeignKey(
        Tax,
        verbose_name='Налог',
        related_name='orders',
        null=True,
        on_delete=models.SET_NULL,
    )
    discount = models.ForeignKey(
        Discount,
        verbose_name='Скидка',
        related_name='orders',
        null=True,
        on_delete=models.SET_NULL,
    )
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        if self.tax:
            total_cost = total_cost + total_cost * self.tax.amount / 100
        if self.discount:
            total_cost = total_cost - total_cost * self.discount.amount / 100
        return total_cost


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='items',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Item,
        verbose_name='Товар',
        related_name='order_items',
        on_delete=models.CASCADE,
    )
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


@receiver(signals.pre_save, sender=Item)
def create_item(sender, instance, **kwargs):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if not instance.stripe_product_id:
        product = stripe.Product.create(
            active=True,
            name=instance.name,
            description=instance.description,
        )
        product_id = product['id']
    else:
        product_id = instance.stripe_product_id

    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(instance.price * 100),
        currency='usd'
    )

    instance.stripe_product_id = product_id
    instance.stripe_price_id = price['id']
