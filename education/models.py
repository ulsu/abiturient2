# -*- coding: utf-8 -*-
from django.db import models

class Direction(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'направление'
        verbose_name_plural = 'направления'


class Faculty(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'факультет'
        verbose_name_plural = 'факультеты'


class EducationForm(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'форма обучения'
        verbose_name_plural = 'формы обучения'


class Exam(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'экзамен'
        verbose_name_plural = 'экзамены'


class Speciality(models.Model):
    direction = models.ForeignKey(Direction, verbose_name='направление')
    faculty = models.ForeignKey(Faculty, verbose_name='факультет')
    education_form = models.ForeignKey(EducationForm, verbose_name='форма обучения')
    exams = models.ManyToManyField(Exam, verbose_name='экзамены')

    def __unicode__(self):
        return '%s - %s (%s)' % (self.faculty.name, self.direction.name, self.education_form.name)

    class Meta:
        verbose_name = 'специальность'
        verbose_name_plural = 'специальности'
        unique_together = ('direction', 'faculty', 'education_form')
