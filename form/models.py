# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from kladr.models import *

class UnicodeIsNameMixin(object):
    def __unicode__(self):
        return self.name

class IDSocialStatus(models.Model, UnicodeIsNameMixin):
    name = models.CharField(max_length=255)


    class Meta:
        verbose_name = 'социальный статус'
        verbose_name_plural = 'социальные статусы'


class Nationality(models.Model, UnicodeIsNameMixin):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'национальность'
        verbose_name_plural = 'национальности'


class MilitaryStatus(models.Model, UnicodeIsNameMixin):
    name=models.CharField(max_length=255)

    class Meta:
        verbose_name = 'военная служба'
        verbose_name_plural = 'военные службы'


class Language(models.Model, UnicodeIsNameMixin):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'иностранный язык'
        verbose_name_plural = 'иностранные языки'

class Citizenship(models.Model, UnicodeIsNameMixin):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'гражданство'
        verbose_name_plural = 'гражданства'


class Application(models.Model):
    GENDER=(
        (1,'Мужской'),
        (2,'Женский'),
    )

    #Персональная информация
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

    #Паспортные данные
    PassportSer     = models.CharField(max_length=4, blank=True, null=True, verbose_name='Серия паспорта')
    PassportNumb    = models.CharField(max_length=6, blank=True, null=True, verbose_name='Номер паспорта')
    CodUVD          = models.CharField(max_length=7,    blank=True, null=True, verbose_name='Код подразделения УВД')
    PassportDate    = models.DateField(                 blank=True, null=True, verbose_name='Дата выдачи паспорта')
    BirthPlace      = models.CharField(max_length=255,  blank=True, verbose_name='Место рождения')
    PassportIssued  = models.CharField(max_length=255,  blank=True, verbose_name='Паспорт выдан')


    RegCountry = models.ForeignKey(Country, blank=True, null=True, verbose_name='Страна')
    RegRegion = models.ForeignKey(Region, blank=True, null=True, verbose_name='Регион')
    RegDistrict = models.ForeignKey(District, blank=True, null=True, verbose_name='Район')
    RegCity = models.ForeignKey(City, blank=True, null=True, verbose_name='Город')
    RegStreet = models.ForeignKey(Street, blank=True, null=True, related_name='+', verbose_name='Улица')
    RegHouse = models.CharField(max_length=255, blank=True, null=True, verbose_name='Дом')
    RegApartment = models.CharField(max_length=255, blank=True, null=True, verbose_name='Квартира')
    RegZipcode = models.IntegerField(max_length=6, blank=True, null=True, verbose_name='Почтовый индекс')

    ResEqualsReg = models.BooleanField(default=True, verbose_name='Прописка и адрес фактического проживания совпадают')

    #Ulyanovsk-city only
    ResStreet = models.ForeignKey(Street, blank=True, null=True, related_name='+', verbose_name='Улица')
    ResHouse = models.CharField(max_length=255, blank=True, null=True, verbose_name='Дом')
    ResApartment = models.CharField(max_length=255, blank=True, null=True, verbose_name='Квартира')
    ResZipcode = models.IntegerField(max_length=6, blank=True, null=True, verbose_name='Почтовый индекс')

    def __unicode__(self):
        return "%s %s %s" % (self.LastName, self.FirstName, self.MiddleName)



class ExamName(models.Model, UnicodeIsNameMixin):
    name = models.CharField(max_length=255)

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