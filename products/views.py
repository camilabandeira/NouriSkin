from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib import messages
from .models import Product, Category, Concern, SkinType, ProductReview
from .forms import ProductForm
from .review_form import ReviewForm


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
    sort_option = request.GET.get('sort')

    products = Product.objects.all()

    if selected_category and selected_category != "None":
        products = products.filter(category__name=selected_category)
    if selected_concern and selected_concern != "None":
        products = products.filter(concern__name=selected_concern)
    if selected_skin_type and selected_skin_type != "None":
        products = products.filter(skin_types__id=selected_skin_type)

    for product in products:
        average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0
        average_rating = round(average_rating)
        product.average_rating = average_rating

    if sort_option == "price-low-to-high":
        products = products.order_by('price')
    elif sort_option == "price-high-to-low":
        products = products.order_by('-price')

    product_count = products.count()

    context = {
        'products': products,
        'categories': categories,
        'concerns': concerns,
        'skin_types': skin_types,
        'selected_category': selected_category,
        'selected_concern': selected_concern,
        'selected_skin_type': selected_skin_type,
        'listed_product_count': products.count(),
        'range': range(1, 6),
        'sort_option': sort_option,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to display the product details """
    product = get_object_or_404(Product, id=product_id)
    
    product_concerns = product.concern.all()
    product_skin_types = product.skin_types.all()
    product_key_ingredients = product.key_ingredients.all()

    filter_option = request.GET.get('filter', 'most-recent')

    if filter_option == 'highest-rating':
        reviews = ProductReview.objects.filter(product=product).order_by('-rating')
    elif filter_option == 'lowest-rating':
        reviews = ProductReview.objects.filter(product=product).order_by('rating')
    else:
        reviews = ProductReview.objects.filter(product=product).order_by('-submitted_at')

    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    for review in reviews:
        review.filled_stars = int(review.rating)

    total_reviews = reviews.count()

    context = {
        'product': product,
        'product_concerns': product_concerns, 
        'product_skin_types': product_skin_types, 
        'product_key_ingredients': product_key_ingredients,  
        'reviews': reviews,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'stars_range': range(1, 6),
    }
    return render(request, 'products/product_detail.html', context)


def write_review(request, product_id):
    """ A view to write a review """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            if request.user.is_authenticated:
                review.user = request.user
                review.name = request.user.get_full_name() or request.user.username
            else:
                review.email = form.cleaned_data.get('email')
                review.name = form.cleaned_data.get('name')
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, "There was an error with your review. Please check the form and try again.")
    else:
        form = ReviewForm(user=request.user)

    context = {
        'product': product,
        'form': form,
    }

    return render(request, 'products/review_form.html', context)


def add_product(request):
    """ A view to add a new product """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})

def product_update(request, pk):
    """ A view to handle updating a product """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/product_update.html', context)

def delete_product(request, product_id):
    """
    A view to delete a product.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('products') 

    return render(request, 'products/delete_product.html', {'product': product})
