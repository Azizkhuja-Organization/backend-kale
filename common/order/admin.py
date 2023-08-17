from django.contrib import admin

from .models import Cart, CartProduct, Order, Wishlist, Comparison, OrderProduct

admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Wishlist)
admin.site.register(Comparison)
