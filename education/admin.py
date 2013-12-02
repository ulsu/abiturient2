# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

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

admin.site.register(Direction, DirectionAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(EducationForm, EducationFormAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Speciality, SpecialityAdmin)