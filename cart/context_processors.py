from decimal import Decimal
from django.conf import settings
from products.models import Product


def cart_contents(request):
    cart_items = []
    total = Decimal("0.00")
    product_count = 0

    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=item_id)
            total += quantity * product.price
            product_count += quantity
            cart_items.append({
                'id': item_id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'total': quantity * product.price,
                'image': product.image.url,
            })
        except Product.DoesNotExist:
            continue

    if total >= settings.FREE_DELIVERY_THRESHOLD:
        delivery = "Free"
        free_delivery_message = None
    else:
        delivery = Decimal(settings.FIXED_DELIVERY_FEE)
        free_delivery_message = (
            f"Spend €{settings.FREE_DELIVERY_THRESHOLD - total:.2f} "
            "more for free delivery"
        )

    grand_total = total if delivery == "Free" else total + delivery

    context = {
        'cart_items': cart_items,
        'total': total.quantize(Decimal("0.01")),
        'product_count': product_count,
        'delivery': (
            delivery if delivery == "Free"
            else delivery.quantize(Decimal("0.01"))
        ),
        'free_delivery_message': free_delivery_message,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total.quantize(Decimal("0.01")),
    }

    return context
