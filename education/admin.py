# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *


class StreamAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EducationFormAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ExamAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SpecialityItemInline(admin.TabularInline):
    model = SpecialityItem
    extra = 0


class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'direction')
    inlines = (SpecialityItemInline,)

class EducationItemAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'direction')

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(EducationItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.rel.to == Speciality:
            field.label_from_instance = self.get_speciality_label
        if db_field.rel.to == SpecialityItem:
            field.label_from_instance = self.get_specialityitem_label
        return field

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(EducationItemAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.rel.to == Speciality:
            field.label_from_instance = self.get_speciality_label
        if db_field.rel.to == SpecialityItem:
            field.label_from_instance = self.get_specialityitem_label
        return field

    def get_speciality_label(self, speciality):
        return speciality.get_full_name()

    def get_specialityitem_label(self, specialityitem):
        return specialityitem.get_full_name()

admin.site.register(Stream, StreamAdmin)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(EducationForm, EducationFormAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(EducationItem, EducationItemAdmin)