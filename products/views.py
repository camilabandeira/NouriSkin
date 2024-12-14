from django.shortcuts import render
from .models import Product, Category, Concern, SkinType


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    categories = Category.objects.all()
    for category in categories:
        category.product_count = Product.objects.filter(category=category).count()

    concerns = Concern.objects.all()
    for concern in concerns:
        concern.product_count = Product.objects.filter(concern=concern).count()

    skin_types = SkinType.objects.all()
    for skin_type in skin_types:
        skin_type.product_count = Product.objects.filter(skin_types=skin_type).count()
        

    selected_category = request.GET.get('category')
    selected_concern = request.GET.get('concern')
    selected_skin_type = request.GET.get('skin_type')


    if selected_category:
        products = Product.objects.filter(category__name=selected_category)
    elif selected_concern:
        products = Product.objects.filter(concern__name=selected_concern)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'concerns': concerns,
        'skin_types': skin_types,
        'selected_category': selected_category,
        'selected_concern': selected_concern,
    }

    return render(request, 'products/products.html', context)