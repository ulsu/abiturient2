# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class IDSocialStatus(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'социальный статус'
        verbose_name_plural = 'социальные статусы'

class IDSocialStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(IDSocialStatus,IDSocialStatusAdmin)


class Nationality(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'национальность'
        verbose_name_plural = 'национальности'

class NationalityAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Nationality,NationalityAdmin)


class MilitaryStatus(models.Model):
    name=models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'военная служба'
        verbose_name_plural = 'военные службы'

class MilitaryStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(MilitaryStatus,MilitaryStatusAdmin)


class Language(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'иностранный язык'
        verbose_name_plural = 'иностранные языки'

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Language,LanguageAdmin)


class Citizenship(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'гражданство'
        verbose_name_plural = 'гражданства'

class CitizenshipAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Citizenship, CitizenshipAdmin)

class Application(models.Model):
    GENDER=(
        (1,'Мужской'),
        (2,'Женский'),
    )

    Edited          = models.BooleanField(default=False)
    user            = models.OneToOneField(User, verbose_name='Пользователь', null=True, blank=True)
    LastName        = models.CharField(max_length=255,  blank=True, verbose_name='Фамилия')
    FirstName       = models.CharField(max_length=255,  blank=True, verbose_name='Имя')
    MiddleName      = models.CharField(max_length=255,  blank=True, verbose_name='Отчество')
    BirthDay        = models.DateField(                 blank=True, null=True, verbose_name='Дата рождения')
    IDSex           = models.PositiveSmallIntegerField( blank=True, null=True, choices=GENDER, verbose_name='Пол')
    IDSocialStatus  = models.ForeignKey(IDSocialStatus, blank=True, null=True, verbose_name='Социальный статус')
    Nationality     = models.ForeignKey(Nationality,    blank=True, null=True, verbose_name='Национальность')
    Citizenship     = models.ForeignKey(Citizenship,    blank=True, null=True, verbose_name='Гражданство')

    PassportSer     = models.CharField(max_length=4, blank=True, null=True, verbose_name='Серия паспорта')
    PassportNumb    = models.CharField(max_length=6, blank=True, null=True, verbose_name='Номер паспорта')
    CodUVD          = models.CharField(max_length=7,    blank=True, null=True, verbose_name='Код подразделения УВД')
    PassportDate    = models.DateField(                 blank=True, null=True, verbose_name='Дата выдачи паспорта')
    BirthPlace      = models.CharField(max_length=255,  blank=True, verbose_name='Место рождения')
    PassportIssued  = models.CharField(max_length=255,  blank=True, verbose_name='Паспорт выдан')

    def __unicode__(self):
        return "%s %s %s" % (self.LastName, self.FirstName, self.MiddleName)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('LastName', 'FirstName', 'MiddleName')
    search_fields = ['LastName', 'FirstName', 'MiddleName']

admin.site.register(Application, ApplicationAdmin)


class ExamName(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class ExamNameAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(ExamName, ExamNameAdmin)


class Exam(models.Model):
    Number   = models.CharField(max_length=20, blank=True, verbose_name='Номер свидетельства ЕГЭ')
    ExamName = models.ForeignKey(ExamName,     blank=True, null = True, verbose_name='Название экзамена')
    Mark     = models.IntegerField(            blank=True, null = True, verbose_name='Оценка')
    DocSer   = models.CharField(max_length=4,  blank=True, null = True, verbose_name='Серия паспорта')
    DocNum   = models.CharField(max_length=6,  blank=True, null = True, verbose_name='Номер паспорта')
    application = models.ForeignKey(Application)

    def __unicode__(self):
        return self.Number

    class Meta:
        verbose_name = 'свидетельство ЕГЭ'
        verbose_name_plural = 'свидетельства ЕГЭ'

class ExamAdmin(admin.ModelAdmin):
    list_display = ('Number', 'ExamName', 'Mark', 'application',)
admin.site.register(Exam, ExamAdmin)