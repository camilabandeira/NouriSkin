from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from products.models import Product
from .forms import OrderForm

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    

    cart_items = []
    for item_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=item_id)
            cart_items.append({
                'product': product,
                'quantity': quantity,
            })
        except Product.DoesNotExist:
            messages.error(request, "One of the products in your cart was not found.")
            return redirect(reverse('products'))
    
    order_form = OrderForm()

    context = {
        'order_form': order_form,
        'cart_items': cart_items, 
    }

    return render(request, 'checkout/checkout.html', context)
