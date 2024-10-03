from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(
        verbose_name='User',
        to=User,
        on_delete=models.CASCADE
    )
    products = models.TextField(
        verbose_name='Products'
    )
    price = models.DecimalField(
        verbose_name='Price',
        max_digits=21,
        decimal_places=2
    )
    status = models.CharField(
        verbose_name='Status',
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('canceled', 'Canceled'),
        ]
    )
    created_at = models.DateTimeField(
        verbose_name='Creation Time',
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f'Order of {self.user.username}'
