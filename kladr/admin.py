# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class CountryAdmin(admin.ModelAdmin):
    list_display = ('title',)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('title',)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('title',)

class CityAdmin(admin.ModelAdmin):
    list_display = ('title',)

class StreetAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Street, StreetAdmin)