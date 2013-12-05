# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('get_name_with_type', 'get_region_admin_link')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_region_admin_link', 'get_district_admin_link')

class StreetAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_region_admin_link', 'get_district_admin_link', 'get_city_admin_link')

admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Street, StreetAdmin)