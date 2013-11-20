# -*- coding: utf-8 -*-
from django.db import models
from form.models import Application


class Country(models.Model):
    title = models.CharField(max_length=255)


class Region(models.Model):
    title = models.CharField(max_length=255)
    full_type = models.CharField(max_length=255)
    short_type = models.CharField(max_length=255)
    zip_code = models.SmallIntegerField(max_length=6)


class District(models.Model):
    title = models.CharField(max_length=255)
    full_type = models.CharField(max_length=255)
    short_type = models.CharField(max_length=255)
    zip_code = models.SmallIntegerField(max_length=6)

    region = models.ForeignKey(Region, related_name='districts')


class City(models.Model):
    title = models.CharField(max_length=255)
    full_type = models.CharField(max_length=255)
    short_type = models.CharField(max_length=255)
    zip_code = models.SmallIntegerField(max_length=6, null=True, blank=True)

    region = models.ForeignKey(Region, related_name='cities')
    district = models.ForeignKey(Region, related_name='+cities', null=True, blank=True)


class Street(models.Model):
    title = models.CharField(max_length=255)
    full_type = models.CharField(max_length=255)
    short_type = models.CharField(max_length=255)
    zip_code = models.SmallIntegerField(max_length=6, null=True, blank=True)

    region = models.ForeignKey(Region, related_name='streets')
    district = models.ForeignKey(Region, related_name='+streets', null=True, blank=True)
    city = models.ForeignKey(City, related_name='streets')


class ResidenceAddress(models.Model):
    application = models.OneToOneField(Application)



