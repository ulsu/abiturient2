# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe

class RegionMixin(object):
    def region(self):
        return Region.objects.get(id=self.id[0:2])

    def get_region_admin_link(self):
        region = self.region()
        if region:
            region_name = '%s %s' % (region.name, region.full_type)
            return mark_safe('<a href="/admin/kladr/region/%s/">%s</a>' % (region.pk, region_name))
        else:
            return 'Нет'
    get_region_admin_link.short_description = 'регион'


class DistrictMixin(object):
    def district(self):
        return District.objects.get(id=self.id[0:5])

    def get_district_admin_link(self):
        district = self.district()
        district_name = '%s %s' % (district.name, district.full_type)
        return mark_safe('<a href="/admin/kladr/district/%s/">%s</a>' % (district.pk, district_name))
    get_district_admin_link.short_description = 'район'


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

class Street(KLADRItem, RegionMixin, DistrictMixin):
    id = models.CharField(max_length=15, verbose_name='КЛАДР ID', primary_key=True)
    class Meta:
        verbose_name = 'улица'
        verbose_name_plural = 'улицы'



