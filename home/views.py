from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def faq_page(request):
    
    return render(request, 'faq.html')
