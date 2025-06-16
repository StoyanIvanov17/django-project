from django.db import models
from django.conf import settings

from project.products.models import Product, Size


class Bag(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class BagItem(models.Model):
    bag = models.ForeignKey(
        Bag,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        unique_together = ('bag', 'product', 'size')
