# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.validators import MinValueValidator

from django.db import models

# Create your models here.
from django.utils import timezone
from cafe.models import Cafe


class Unit(models.Model):
    name = models.CharField(
        verbose_name=u"Название",
        max_length=255
    )
    entry = models.CharField(
        verbose_name=u"Обозначение",
        max_length=255
    )
    active = models.BooleanField(
        verbose_name=u"Активна?",
        default=False
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Единица измерения"
        verbose_name_plural = u"Единицы измерения"


class StockItem(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        verbose_name="Кафе",
    )
    unit = models.ForeignKey(
        Unit,
        verbose_name=u"Единица измерения",
        blank=True,
        null=True
    )
    name = models.CharField(
        verbose_name=u"Название",
        max_length=255
    )
    quantity = models.IntegerField(
        verbose_name=u"Количество на складе",
        default=0,
        validators=[MinValueValidator(0)]
    )
    consumption = models.FloatField(
        verbose_name=u"Расход в день (гипотетический)",
        validators=[MinValueValidator(0)],

    )
    active = models.BooleanField(
        verbose_name=u"Активен?",
        default=False
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Продукт"
        verbose_name_plural = u"Продукты"


class SpentStockItem(models.Model):
    stock_item = models.ForeignKey(
        StockItem,
        verbose_name="Продукт"
    )

    unit = models.ForeignKey(
        Unit,
        verbose_name=u"Единица измерения",
        blank=True,
        null=True
    )

    quantity = models.IntegerField(
        verbose_name=u"Сколько потрачено",
        validators=[MinValueValidator(0)]
    )
    date = models.DateTimeField(
        verbose_name=u"Дата",
        default=timezone.now
    )

    class Meta:
        verbose_name = u"Запись о расходах"
        verbose_name_plural = u"Записи о расходах"