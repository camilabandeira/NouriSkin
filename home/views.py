from django.shortcuts import render, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from products.models import Product, ProductReview
from django.db.models import Avg




def homepage(request):
    """Render the homepage"""
    best_sellers_list = Product.objects.filter(rating__gte=4.0).order_by('-rating')
    paginator = Paginator(best_sellers_list, 4)  
    page_number = request.GET.get('page')
    best_sellers = paginator.get_page(page_number)


    for product in best_sellers:
        avg_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0
        product.rating = round(avg_rating, 1)
        product.full_stars = range(int(product.rating)) 
        product.empty_stars = range(6 - int(product.rating))  
        product.save()


    context = {
        'best_sellers': best_sellers,
        'paginator': paginator,
        'current_page': best_sellers.number,
    }
    return render(request, 'homepage.html', context)


def faq_page(request):
    """Render the FAQ page"""
    return render(request, 'faq.html')

def return_refund(request):
    """Render the Return & Refund page"""
    return render(request, 'return_refund.html')

def custom_404_view(request, exception):
    """Render the 404 page"""
    return render(request, '404.html', status=404)

def about(request):
    """Render the About page"""
    return render(request, 'about.html')

def contact(request):
    """Render the Contact page"""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print(f"Name: {name}, Email: {email}, Message: {message}")

        return HttpResponseRedirect(reverse("contact") + "?success=1")

    return render(request, "contact.html")