# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db.models import Q
from django.db import models
from django.utils import timezone
from cafe.utils import get_timezone_choices, get_minutes, make_summary_entry


class Cafe(models.Model):
    name = models.CharField(
        verbose_name=u"Название кафе",
        max_length=255,
    )
    timezone = models.CharField(
        verbose_name=u"Временная зона",
        choices=get_timezone_choices(),
        max_length=255,
        default=timezone.get_current_timezone().localize(datetime.datetime(2015, 1, 1)).strftime('%z')
    )

    @models.permalink
    def get_absolute_url(self):
        return 'cafe:cafe-detail', {}, {'pk': self.id}

    def get_title(self):
        return self.name

    def get_breadcrumbs(self):
        return [{"title": self.get_title()}]

    def get_tables(self):
        return Table.objects.filter(cafe=self, active=True)

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
        ordering = ['time_start']


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

    def get_title(self):
        return self.name

    def get_active_visit(self):
        visits = Visit.objects.filter(table=self, active=True)
        if visits:
            return visits[0]
        else:
            return None

    def make_new_visit(self):
        if self.get_active_visit():
            return False
        else:
            Visit.objects.create(table=self, active=True)
            return True

    def end_active_visit_and_calculate(self):
        if self.get_active_visit():
            self.get_active_visit().finalize()
            return True
        else:
            return False

    def cancel_visit(self):
        if self.get_active_visit():
            self.get_active_visit().cancel()
            return True
        else:
            return False

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

    # def calculate(self):
    #     self.summary = self.end - self.start

    def cancel(self):
        self.delete()

    def get_time_shift(self):
        shift = self.table.cafe.timezone
        hours = int(shift[:3])
        minutes = int(shift[3:])
        return datetime.timedelta(hours=hours, minutes=minutes)

    def get_rate_periods_before_midnigth(self):
        return RatePeriod.objects.filter(
            time_end_gte=(self.start + self.get_time_shift()).time()
        )

    def get_rate_periods_from_midnight(self):
        return RatePeriod.objects.filter(
            time_start_lte=(self.end + self.get_time_shift()).time()
        )

    def get_rate_periods(self):
        time_shift = self.get_time_shift()
        return RatePeriod.objects.filter(
            time_end__gte=(self.start + time_shift).time(),
            time_start__lte=(self.end + time_shift).time(),
            rate=self.table.rate
        )

    def get_all_rate_periods(self):
        return RatePeriod.objects.filter(rate=self.table.rate)

    # рассчитываем стоимость посещения.
    def finalize(self):
        # время окончания посещения
        self.end = timezone.now()

        # стоимость минуты по-умолчанию
        default_price = self.table.rate.default_price

        # итоговая стоимость посещения
        total_cost = 0

        # массив элеметнов для сводки о посещении
        summary = []

        # выясняем, если посещение длилось втечение нескольких календарных дней
        days = (self.end - self.start).days

        summary.append(u"Расчёт от %s \n\n" % self.end)

        if days > 0:
            # выясняем, сколько дней длилось посещение
            spent_full_days = days - 1

            # находим "цены в периоде", которые нужно учесть в первый день посещения
            rate_periods_start = self.get_rate_periods_before_midnigth()

            # находим "цены в периоде", которые нужно учесть в последний день посещения
            rate_periods_end = self.get_rate_periods_from_midnight()

            # prev_time используется при итерации по "ценам в периоде"
            # изначально выставляется на значение начала посещения
            prev_time = (self.start + self.get_time_shift()).time()

            # рассчитываем стоимость посещения в первый день
            if rate_periods_start:

                # считаем стоимость по "ценам в периоде" и по промежуткам, в которых цена по-умолчанию
                for rate_period in rate_periods_start:
                    cost = get_minutes(prev_time, rate_period.time_start) * default_price
                    summary.append(make_summary_entry(cost, prev_time, rate_period.time_start, default_price))
                    total_cost += cost

                    cost = get_minutes(rate_period.time_start, rate_period.time_end) * rate_period.price
                    summary.append(make_summary_entry(cost, rate_period.time_start, rate_period.time_end, rate_period.price))
                    total_cost += cost

                    prev_time = rate_period.time_end

            # считаем стоимость посещения до полуночи
            cost = get_minutes(prev_time, datetime.time(), False) * default_price
            summary.append(make_summary_entry(cost, prev_time, datetime.time(), default_price))
            total_cost += cost

            # считаем стоимость посещений, которые длились целые сутки
            if spent_full_days:
                day_cost = 0
                all_rate_periods = self.get_all_rate_periods()
                summary.append("uРасчёт c %s по %s \n детализация за день:\n") % (
                    (self.end + datetime.timedelta(days=1)),
                    (self.end + datetime.timedelta(days=spent_full_days))
                )

                if all_rate_periods:
                    prev_time = datetime.time()
                    for rate_period in all_rate_periods:
                        cost = get_minutes(prev_time, rate_period.time_start) * default_price
                        summary.append(make_summary_entry(cost, prev_time, rate_period.time_start, default_price))
                        day_cost += cost

                        cost = get_minutes(rate_period.time_start, rate_period.time_end) * rate_period.price
                        summary.append(make_summary_entry(cost, rate_period.time_start, rate_period.time_end, rate_period.price))
                        day_cost += cost

                        prev_time = rate_period.time_end

                    cost -= get_minutes(prev_time, datetime.time(), False) * default_price
                    summary.append(make_summary_entry(cost, prev_time, datetime.time().time_start, default_price))
                    day_cost += cost
                else:

                    day_cost = 1440 * default_price
                    summary.append("uРасчёт произведенё по цене по-умолчанию, составляющей %s по %s Р.\n" % default_price)
                days_cost = day_cost * spent_full_days
                summary.append("За %s дней начислено %s Р.\n общей стоимостью %s Р.\n" % (spent_full_days,day_cost, days_cost))
                total_cost += day_cost
            # считаем стоимость посещений в последний день
            if rate_periods_end:
                prev_time = datetime.time()
                for rate_period in self.get_all_rate_periods():
                    cost = get_minutes(prev_time, rate_period.time_start) * default_price
                    summary.append(make_summary_entry(cost, prev_time, rate_period.time_start, default_price))
                    total_cost += cost

                    cost = get_minutes(rate_period.time_start, rate_period.time_end) * rate_period.price
                    summary.append(make_summary_entry(cost, rate_period.time_start, rate_period.time_end, rate_period.price))
                    total_cost += cost

                end_time = (self.end + self.get_time_shift()).time()
                cost = get_minutes(prev_time, end_time) * default_price
                summary.append(make_summary_entry(cost, prev_time, end_time, default_price))
                total_cost += cost
        else:
            rate_periods = self.get_rate_periods()
            prev_time = (self.start + self.get_time_shift()).time()
            for rate_period in rate_periods:
                cost = get_minutes(prev_time, rate_period.time_start) * default_price
                summary.append(make_summary_entry(cost, prev_time, rate_period.time_start, default_price))
                total_cost += cost


                cost = get_minutes(rate_period.time_start, rate_period.time_end) * rate_period.price
                summary.append(make_summary_entry(cost, rate_period.time_start, rate_period.time_end, rate_period.price))
                total_cost += cost
                prev_time = rate_period.time_end

            end_time = (self.end + self.get_time_shift()).time()
            cost = get_minutes(prev_time, end_time) * default_price
            summary.append(make_summary_entry(cost, prev_time, end_time, default_price))
            total_cost += cost
            summary.append(u"\n итого к оплате %s Р." % total_cost)
        self.total_cost = total_cost
        self.summary = "".join(summary)
        self.active = False
        self.save()

    def __unicode__(self):
        # TODO: format start and end
        return u"Посещение за столиком '%s' с %s по %s" % (self.table.name,self.start, self.end )