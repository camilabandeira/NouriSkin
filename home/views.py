from django.shortcuts import render, HttpResponseRedirect, reverse

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

def contact(request):
    """Render the Contact page"""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print(f"Name: {name}, Email: {email}, Message: {message}")

        return HttpResponseRedirect(reverse("contact") + "?success=1")

    return render(request, "contact.html")