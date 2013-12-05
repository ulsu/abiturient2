# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class PolymorphicModel(models.Model):
    content_type = models.ForeignKey(ContentType, null=True, blank=True, editable=False)
    actual_object_id = models.PositiveIntegerField(null=True, blank=True, editable=False)
    actual_instance = generic.GenericForeignKey("content_type", "actual_object_id")
    def save(self, *args, **kwargs):
        super(PolymorphicModel, self).save(*args, **kwargs)
        if not self.actual_object_id:
            self.actual_instance = self
            super(PolymorphicModel, self).save()
    class Meta:
        abstract = True


class TileSet(models.Model):
    slug = models.SlugField(verbose_name='test')
    title = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title


class Tile(PolymorphicModel):
    title = models.CharField(max_length=255)
    set = models.ForeignKey(TileSet, related_name='Tile')
    order = models.IntegerField(max_length=255)


class LinkTile(Tile):
    href = models.CharField(max_length=255)
    def display(self):
        return self.href

class FileTile(Tile):
    document = models.FileField(upload_to='/media/tile/')
    def display(self):
        return self.document


class ContentTile(Tile):
    content = models.TextField(blank=True, null=True)
    def display(self):
        return '/tiles/%s/%s/' % (self.set.slug, self.pk)
