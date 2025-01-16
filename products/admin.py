from django.contrib import admin
from .models import Category, Product, Concern, ProductReview, KeyIngredient, SkinType


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ConcernAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class SkinTypeAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )
    ordering = ('name',)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'submitted_at')
    list_filter = ('product', 'rating', 'skin_type', 'age_group')
    search_fields = ('name', 'review_text')


class KeyIngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Concern, ConcernAdmin)
admin.site.register(SkinType, SkinTypeAdmin)
admin.site.register(KeyIngredient, KeyIngredientAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
