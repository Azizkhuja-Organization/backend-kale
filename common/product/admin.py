from django.contrib import admin

from .models import Category, Product, SubCategory, ProductImage

admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
