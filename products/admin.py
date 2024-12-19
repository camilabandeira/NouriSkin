from django.contrib import admin
from .models import Category, Product, Concern, ProductReview


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

class ConcerAdmin(admin.ModelAdmin):
    list_display = (
         'friendly_name',
        'name',
        )
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'submitted_at')  
    list_filter = ('product', 'rating', 'skin_type', 'age_group')  
    search_fields = ('name', 'review_text')  
 

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Concern, ConcerAdmin)
admin.site.register(ProductReview, ProductReviewAdmin) 
