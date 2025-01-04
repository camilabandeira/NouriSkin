
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Product, ProductReview

@receiver(post_save, sender=ProductReview)
@receiver(post_delete, sender=ProductReview)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    avg_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0
    product.rating = round(avg_rating, 1)
    product.save()
