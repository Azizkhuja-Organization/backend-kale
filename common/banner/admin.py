from django.contrib import admin

from .models import Banner, SmallBanner, HeaderDiscount

admin.site.register(Banner)
admin.site.register(SmallBanner)


@admin.register(HeaderDiscount)
class HeaderDiscountAdmin(admin.ModelAdmin):
    list_display = ["text", "enabled"]
