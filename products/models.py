from django.db import models
from django.contrib.auth.models import User


class ProductReview(models.Model):
    class Meta:
        verbose_name_plural = "Product Reviews"

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
    )
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    skin_type = models.CharField(
        max_length=50,
        choices=[
            ('Normal', 'Normal'),
            ('Combination', 'Combination'),
            ('Oily', 'Oily'),
            ('Dry', 'Dry'),
        ],
    )
    age_group = models.CharField(
        max_length=50,
        choices=[
            ('25-34', '25-34'),
            ('35-44', '35-44'),
            ('45-54', '45-54'),
            ('55+', '55+'),
        ],
    )

    def __str__(self):
        return f"{self.title} by {self.name or self.user.username}"


class SkinType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Skin Types"

    def __str__(self):
        return self.friendly_name or self.name


class Concern(models.Model):
    name = models.CharField(max_length=100, unique=True)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Concerns"

    def __str__(self):
        return self.name


class KeyIngredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Key Ingredients"

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100, unique=True)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    concern = models.ManyToManyField(Concern, blank=True)
    skin_types = models.ManyToManyField(
        'SkinType',
        related_name='products',
        blank=True,
    )
    key_ingredients = models.ManyToManyField(
        'KeyIngredient',
        related_name='products',
        blank=True,
    )
    how_to_use = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name
