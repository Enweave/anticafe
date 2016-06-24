# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.validators import MinValueValidator

from django.db import models
from django.db.models.signals import post_save
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

    def get_spent_stock_items(self):
        return SpentStockItem.objects.filter(stock_item=self)

    def get_current_quantity(self):
        spent_items = SpentStockItem.objects.filter(stock_item=self, date__date=timezone.now().date()).order_by("id")
        if spent_items:
            return list(spent_items.values_list("current_quantity", flat=True))[-1]
        else:
            return self.quantity

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Продукт"
        verbose_name_plural = u"Продукты"


class SpentStockItem(models.Model):
    stock_item = models.ForeignKey(
        StockItem,
        verbose_name="Продукт",
        validators=[MinValueValidator(0)]
    )

    unit = models.ForeignKey(
        Unit,
        verbose_name=u"Единица измерения",
        blank=True,
        null=True
    )

    quantity = models.IntegerField(
        verbose_name=u"изменение",
    )

    current_quantity = models.IntegerField(
        verbose_name=u"текущее значение",
    )

    date = models.DateTimeField(
        verbose_name=u"Дата",
        default=timezone.now
    )

    def __unicode__(self):
        return u"%s x %s" % (self.stock_item.name, self.quantity)

    class Meta:
        verbose_name = u"Запись о расходах"
        verbose_name_plural = u"Записи о расходах"


from django.dispatch import receiver

@receiver(post_save, sender=StockItem)
def stock_post_save(sender, **kwargs):
    if kwargs.get("created", False):
        instance = kwargs.get("instance")

        new_spent_stock = SpentStockItem(
            stock_item=instance,
            unit=instance.unit,
            quantity=instance.quantity,
            current_quantity=instance.quantity
        )
        new_spent_stock.save()
