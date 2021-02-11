from django import template

register = template.Library()

def in_cart(product, cart):
    keys = cart.keys()
    print(keys)
