# -*- coding: utf-8 -*-
from django.db import models


class Country(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title


class Region(models.Model):
    title = models.CharField(max_length=255)
    full_type = models.CharField(max_length=255)
    short_type = models.CharField(max_length=255)
    zip_code = models.SmallIntegerField(max_length=6)

    def __unicode__(self):
        return self.title

class District(models.Model):
    title = models.CharField(max_length=255)
    full_type = models.CharField(max_length=255)
    short_type = models.CharField(max_length=255)
    zip_code = models.SmallIntegerField(max_length=6)

    region = models.ForeignKey(Region, related_name='districts')

    def __unicode__(self):
        return self.title



class City(models.Model):
    title = models.CharField(max_length=255)
    full_type = models.CharField(max_length=255)
    short_type = models.CharField(max_length=255)
    zip_code = models.SmallIntegerField(max_length=6, null=True, blank=True)

    region = models.ForeignKey(Region, related_name='cities')
    district = models.ForeignKey(District, related_name='cities', null=True, blank=True)

    def __unicode__(self):
        return self.title


class Street(models.Model):
    title = models.CharField(max_length=255)
    full_type = models.CharField(max_length=255)
    short_type = models.CharField(max_length=255)
    zip_code = models.SmallIntegerField(max_length=6, null=True, blank=True)

    region = models.ForeignKey(Region, related_name='streets')
    district = models.ForeignKey(District, related_name='streets', null=True, blank=True)
    city = models.ForeignKey(City, related_name='streets')

    def __unicode__(self):
        return self.title



