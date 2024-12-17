from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Concern, SkinType


def all_products(request):
    """ A view to show all products """

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

    products = Product.objects.all()
    if selected_category:
        products = products.filter(category__name=selected_category)
    if selected_concern:
        products = products.filter(concern__name=selected_concern)
    if selected_skin_type:
        products = products.filter(skin_types__id=selected_skin_type) 

    product_count = products.count()

    context = {
        'products': products,
        'categories': categories,
        'concerns': concerns,
        'skin_types': skin_types,
        'selected_category': selected_category,
        'selected_concern': selected_concern,
        'selected_skin_type': selected_skin_type,
        'product_count': product_count,
    }

    return render(request, 'products/products.html', context)



def product_detail(request, product_id):
    """ A view to display the product details """
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


def write_review(request, product_id):
    """ A view to write a review """
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/review_form.html', {'product': product})
