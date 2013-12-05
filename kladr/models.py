# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe
from main.utils import get_or_none

class RegionMixin(object):
    def region(self):
        return get_or_none(Region, **{'id':self.id[0:2]})

    def get_region_admin_link(self):
        region = self.region()
        if region is not None:
            region_name = '%s %s' % (region.name, region.full_type)
            return mark_safe('<a href="/admin/kladr/region/%s/">%s</a>' % (region.pk, region_name))
        else:
            return 'Нет'
    get_region_admin_link.short_description = 'регион'


class DistrictMixin(object):
    def district(self):
        return get_or_none(District, **{'id':self.id[0:5]})

    def get_district_admin_link(self):
        district = self.district()
        if district is not None:
            district_name = '%s %s' % (district.name, district.full_type)
            return mark_safe('<a href="/admin/kladr/district/%s/">%s</a>' % (district.pk, district_name))
        else:
            return 'Нет'
    get_district_admin_link.short_description = 'район'


class CityMixin(object):
    def city(self):
        return get_or_none(City, **{'id':self.id[0:11]})

    def get_city_admin_link(self):
        city = self.city()
        if city is not None:
            city_name = '%s %s' % (city.full_type, city.name)
            return mark_safe('<a href="/admin/kladr/city/%s/">%s</a>' % (city.pk, city_name))
        else:
            return 'Нет'
    get_city_admin_link.short_description = 'город'


class KLADRItem(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    full_type = models.CharField(max_length=255, verbose_name='полный тип')
    short_type = models.CharField(max_length=255, verbose_name='краткий тип')

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def get_name_with_type(self):
        return '%s %s' % (self.name, self.full_type)
    get_name_with_type.short_description = 'название'


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'


class Region(KLADRItem):
    id = models.CharField(max_length=2, verbose_name='КЛАДР ID', primary_key=True)
    class Meta:
        verbose_name = 'регион'
        verbose_name_plural = 'регионы'


class District(KLADRItem, RegionMixin):
    id = models.CharField(max_length=5, verbose_name='КЛАДР ID', primary_key=True)
    class Meta:
        verbose_name = 'районы'
        verbose_name_plural = 'районы'


class City(KLADRItem, RegionMixin, DistrictMixin):
    id = models.CharField(max_length=11, verbose_name='КЛАДР ID', primary_key=True)
    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

class Street(KLADRItem, RegionMixin, DistrictMixin, CityMixin):
    id = models.CharField(max_length=15, verbose_name='КЛАДР ID', primary_key=True)
    class Meta:
        verbose_name = 'улица'
        verbose_name_plural = 'улицы'



