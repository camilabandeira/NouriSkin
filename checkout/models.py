import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from decimal import Decimal
from products.models import Product
from profiles.models import Profile
from django_countries.fields import CountryField


class Order(models.Model):
    order_number = models.CharField(
        max_length=32, null=False, editable=False
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='orders'
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(
        blank_label='Select Country', null=False, blank=False
    )
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=''
    )

    def _generate_order_number(self):
        """Generate a unique order number using UUID."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update order total, delivery cost, and grand total."""
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total')
        )['lineitem_total__sum'] or 0

        free_delivery_threshold = Decimal(settings.FREE_DELIVERY_THRESHOLD)
        fixed_delivery_fee = Decimal(settings.FIXED_DELIVERY_FEE)

        if self.order_total < free_delivery_threshold:
            self.delivery_cost = fixed_delivery_fee
        else:
            self.delivery_cost = Decimal('0.00')

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """Override the save method to set the order number."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """Override the save method to calculate lineitem total."""
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} on order {self.order.order_number}'
