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

class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'direction', 'education_form')

class EducationItemAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'direction')

admin.site.register(Stream, StreamAdmin)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(EducationForm, EducationFormAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(EducationItem, EducationItemAdmin)