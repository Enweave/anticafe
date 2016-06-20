# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.validators import MinValueValidator

from django.db import models

# Create your models here.
from django.utils import timezone
from cafe.utils import get_timezone_choices


class Cafe(models.Model):
    name = models.CharField(
        verbose_name=u"Название кафе",
        max_length=255
    )
    timezone = models.CharField(
        verbose_name=u"Временная зона",
        choices=get_timezone_choices(),
        max_length=255
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Кафе"
        verbose_name_plural = u"Кафе"


class Rate(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        verbose_name="Кафе",
    )
    name = models.CharField(
        verbose_name=u"Название тарифа",
        max_length=255
    )
    default_price = models.FloatField(
        verbose_name=u"Цена в минуту по-умолчанию",
        validators=[MinValueValidator(0)]
    )

    def __unicode__(self):
        return self.name

    def get_periods(self):
        return RatePeriod.objects.filter(rate=self)

    class Meta:
        verbose_name = u"Тариф"
        verbose_name_plural = u"Тарифы"


class RatePeriod(models.Model):
    rate = models.ForeignKey(
        Rate,
        verbose_name=u"Тариф"
    )
    time_start = models.TimeField(
        verbose_name=u'Время начала',
    )
    time_end = models.TimeField(
        verbose_name=u'Время окончания',
    )
    price = models.FloatField(
        verbose_name=u"Цена в минуту",
        validators=[MinValueValidator(0)]
    )

    def __unicode__(self):
        return u"%s [%s|%s]" % (self.rate.name, self.time_start, self.time_end)

    class Meta:
        verbose_name = u"Цена в периоде"
        verbose_name_plural = u"Цены в периоде"


class Table(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        verbose_name="Кафе",
    )
    rate = models.ForeignKey(
        Rate,
        verbose_name=u"Тариф"
    )
    name = models.CharField(
        verbose_name=u"Название стола",
        max_length=255
    )
    active = models.BooleanField(
        verbose_name=u"Активен?",
        default=False
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Столик"
        verbose_name_plural = u"Столики"


class Visit(models.Model):
    table = models.ForeignKey(
        Table,
        verbose_name="Столик",
    )
    active = models.BooleanField(
        verbose_name=u"Активно?",
        default=False
    )
    start = models.DateTimeField(
        verbose_name=u"Начало",
        default=timezone.now
    )
    end = models.DateTimeField(
        verbose_name=u"Окончание",
        blank=True,
        null=True
    )
    total_cost = models.FloatField(
        verbose_name=u"Итоговая стоимость",
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    summary = models.TextField(
        verbose_name=u"сводка",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = u"Посещение"
        verbose_name_plural = u"Посещения"

    def __unicode__(self):
        # TODO: format start and end
        return u"Посещение за столиком '%s' с %s по %s" % (self.table.name,self.start, self.end )