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

