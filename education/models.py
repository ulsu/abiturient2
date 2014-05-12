# -*- coding: utf-8 -*-
from django.db import models
from form.models import Application


class UnicodeIsName(object):
    def __unicode__(self):
        return self.name


class Direction(models.Model, UnicodeIsName):
    name = models.CharField(max_length=255, verbose_name='название')

    class Meta:
        verbose_name = 'направление'
        verbose_name_plural = 'направления'


class Stream(models.Model, UnicodeIsName):
    name = models.CharField(max_length=255, verbose_name='название')

    class Meta:
        verbose_name = 'поток'
        verbose_name_plural = 'потоки'


class Faculty(models.Model, UnicodeIsName):
    name = models.CharField(max_length=255, verbose_name='название')

    class Meta:
        verbose_name = 'факультет'
        verbose_name_plural = 'факультеты'


class EducationForm(models.Model, UnicodeIsName):
    name = models.CharField(max_length=255, verbose_name='название')

    class Meta:
        verbose_name = 'форма обучения'
        verbose_name_plural = 'формы обучения'


class Exam(models.Model, UnicodeIsName):
    name = models.CharField(max_length=255, verbose_name='название')

    class Meta:
        verbose_name = 'экзамен'
        verbose_name_plural = 'экзамены'


class Speciality(models.Model):
    direction = models.ForeignKey(Direction, verbose_name='направление')
    faculty = models.ForeignKey(Faculty, verbose_name='факультет')
    education_forms = models.ManyToManyField(EducationForm, verbose_name='формы обучения', through='SpecialityItem')

    def __unicode__(self):
        return self.faculty.name

    def get_full_name(self):
        return '%s - %s' % (self.direction.name, self.faculty.name)

    class Meta:
        verbose_name = 'специальность'
        verbose_name_plural = 'специальности'
        unique_together = ('direction', 'faculty')


class SpecialityItem(models.Model):
    speciality = models.ForeignKey(Speciality, verbose_name='специальность')
    education_form = models.ForeignKey(EducationForm, verbose_name='форма обучения')
    exams = models.ManyToManyField(Exam, verbose_name='экзамены')

    def __unicode__(self):
        return self.education_form.name

    def get_full_name(self):
        return '%s - %s' % (self.speciality.faculty.name, self.education_form.name)

    class Meta:
        verbose_name = 'форма обучения'
        verbose_name_plural = 'формы обучения'
        unique_together = ('speciality', 'education_form')


class EducationItem(models.Model):
    application = models.ForeignKey(Application, null=True, blank=True)
    direction = models.ForeignKey(Direction, verbose_name='направление', null=True, blank=True)
    faculty = models.ForeignKey(Speciality, verbose_name='факультет', null=True, blank=True)
    education_form = models.ManyToManyField(SpecialityItem, verbose_name='формы обучения', null=True, blank=True)
    stream = models.ForeignKey(Stream, verbose_name='поток', null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order',]