from django.contrib import admin

from .models import Address, Region, Street, District


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    ...


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    ...


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    ...


admin.site.register(Address)
