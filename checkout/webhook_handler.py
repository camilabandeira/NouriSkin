from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product

import stripe
import json


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        intent = event.data.object
        pid = intent.id
        metadata = intent.metadata
        bag = metadata.get('bag', '{}')
        shipping_details = intent.shipping
        grand_total = round(intent.amount_received / 100, 2)

        shipping_details.address = {
            k: v or None for k, v in shipping_details.address.items()
        }

        order = self._get_or_create_order(pid, bag, shipping_details, grand_total)

        if order:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS',
                status=200
            )
        else:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR',
                status=500
            )

    def _get_or_create_order(self, pid, bag, shipping_details, grand_total):
        """Retrieve or create the order"""
        try:
            order = Order.objects.get(stripe_pid=pid)
            return order
        except Order.DoesNotExist:
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=shipping_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    stripe_pid=pid,
                    original_bag=bag,
                )
                # Add line items to the order
                self._add_order_line_items(order, bag)
                return order
            except Exception as e:
                if order:
                    order.delete()
                return None

    def _add_order_line_items(self, order, bag):
        """Add line items to the order"""
        for item_id, item_data in json.loads(bag).items():
            product = Product.objects.get(id=item_id)
            if isinstance(item_data, int):
                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data,
                )
            else:
                for size, quantity in item_data['items_by_size'].items():
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        product_size=size,
                    )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
