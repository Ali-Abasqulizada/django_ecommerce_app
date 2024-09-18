from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product

@receiver(post_save, sender=Product)
def update_category_product_count_on_save(sender, instance, **kwargs):
    if instance.category and instance.change_category_count:
        instance.category.increase_product_count_by_one()

@receiver(post_delete, sender=Product)
def update_category_product_count_on_delete(sender, instance, **kwargs):
    if instance.category and instance.change_category_count:
        instance.category.decrease_product_count_by_one()
