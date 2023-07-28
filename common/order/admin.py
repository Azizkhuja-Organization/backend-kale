from django.contrib import admin

from .models import Cart, CartProduct, Checkout, Order, Wishlist

admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Checkout)
admin.site.register(Order)
admin.site.register(Wishlist)
