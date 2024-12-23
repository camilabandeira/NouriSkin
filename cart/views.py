from django.shortcuts import render, redirect
from django.contrib import messages
def view_cart(request):
    """ A view that renders the cart contents page """
    return render(request, 'cart/cart.html')

def add_to_cart(request, item_id):
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    item_id = str(item_id)

    if item_id in cart:
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    request.session.modified = True

    messages.success(request, "Item added to cart!")


    return redirect(redirect_url)

def update_cart(request, item_id):
    """ Update the quantity of the specified product to the specified amount """
    action = request.POST.get('action', None)
    cart = request.session.get('cart', {})

    item_id = str(item_id)

    if action == 'decrease':
        if item_id in cart and cart[item_id] > 1:
            cart[item_id] -= 1
        elif item_id in cart:
            del cart[item_id]
    elif action == 'increase':
        if item_id in cart:
            cart[item_id] += 1
        else:
            cart[item_id] = 1
    elif action == 'remove':
        if item_id in cart:
            del cart[item_id]
            messages.success(request, "Item removed from the cart.")

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')
