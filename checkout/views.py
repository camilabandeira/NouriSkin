import os
import json
from decimal import Decimal

from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

import stripe

from .forms import OrderForm
from .models import OrderLineItem, Order, Profile
from cart.context_processors import cart_contents
from products.models import Product


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': str(request.user),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            "Sorry, your payment cannot be processed right now. "
            "Please try again later."
        )
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = os.getenv('STRIPE_PUBLIC_KEY', '')
    stripe_secret_key = os.getenv('STRIPE_SECRET_KEY', '')

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(
                request, "There's nothing in your bag at the moment"
            )
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

            if request.user.is_authenticated:
                profile = Profile.objects.get(user=request.user)
                order.profile = profile

                if 'save_info' in request.POST:
                    profile.default_phone_number = form_data['phone_number']
                    profile.default_country = form_data['country']
                    profile.default_postcode = form_data['postcode']
                    profile.default_town_or_city = form_data['town_or_city']
                    profile.default_street_address1 = form_data[
                        'street_address1']
                    profile.default_street_address2 = form_data[
                        'street_address2']
                    profile.default_county = form_data['county']
                    profile.save()

            order.save()
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()

            for item_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "One of the products in your cart was not found."
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

            order.update_total()
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(
                request,
                "There was an error with your form. "
                "Please double-check your information."
            )

    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(
                request, "There's nothing in your bag at the moment"
            )
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
                messages.error(
                    request,
                    "One of the products in your cart was not found."
                )
                return redirect(reverse('products'))

        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                initial_data = {
                    'full_name': (
                        f"{request.user.first_name} {request.user.last_name}"
                    ),
                    'email': request.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                }
                order_form = OrderForm(initial=initial_data)
            except Profile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        context = {
            'form': order_form,
            'cart_items': cart_items,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(
        request,
        f"Order successfully processed! Your order number is {order_number}. "
        f"A confirmation email will be sent to {order.email}."
    )

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
