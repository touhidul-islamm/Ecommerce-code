from django import template
from store.models import Order
register=template.Library()
@register.filter
def cart_count(user):
    if user.is_authenticated:
        cart_count=Order.objects.filter(user=user, ordered=False)
        if cart_count.exists():
            return cart_count[0].cart_product.count()
        return 0
    return 0