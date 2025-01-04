from django.shortcuts import render

def homepage(request):
    """Render the homepage"""
    return render(request, 'homepage.html')

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