from django.contrib import admin
from models import *

class IDSocialStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


class NationalityAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MilitaryStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CitizenshipAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('LastName', 'FirstName', 'MiddleName')
    search_fields = ['LastName', 'FirstName', 'MiddleName']

class ExamNameAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ExamAdmin(admin.ModelAdmin):
    list_display = ('Number', 'ExamName', 'Mark', 'application',)


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Citizenship, CitizenshipAdmin)
admin.site.register(Language,LanguageAdmin)
admin.site.register(MilitaryStatus,MilitaryStatusAdmin)
admin.site.register(Nationality,NationalityAdmin)
admin.site.register(IDSocialStatus, IDSocialStatusAdmin)
admin.site.register(ExamName, ExamNameAdmin)
admin.site.register(Exam, ExamAdmin)

