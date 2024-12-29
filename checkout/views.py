import os

from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
import json
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

import stripe

from .forms import OrderForm
from .models import OrderLineItem, Order
from cart.context_processors import cart_contents
from products.models import Product

require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)

def checkout(request):
    stripe_public_key = os.getenv('STRIPE_PUBLIC_KEY', '')
    stripe_secret_key = os.getenv('STRIPE_SECRET_KEY', '')

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            for item_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(quantity, int):
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                        )
                    else:
                        for size, qty in quantity.items():
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                quantity=qty,
                                product_size=size,
                            )
                except Product.DoesNotExist:
                    messages.error(request, "One of the products in your cart was not found.")
                    order.delete()
                    return redirect(reverse('view_cart'))

            order.update_total()
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double-check your information.')

    else:
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

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

        context = {
            'order_form': order_form,
            'cart_items': cart_items,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    save_info = request.session.get('save_info')
    order = Order.objects.get(order_number=order_number)

    messages.success(request, f'Order successfully processed! Your order number is {order_number}. A confirmation email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
