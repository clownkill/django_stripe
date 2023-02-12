from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
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
