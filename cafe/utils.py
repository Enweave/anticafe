# -*- coding: utf-8 -*-

import datetime
import pytz


def get_timezone_choices():
    """
        получить временные зоны для selectbox в админ панели
    :return: list of tuples
    """
    choices = []

    # Берём из библиотеки
    for tz in pytz.common_timezones:

        # получаем смещение
        shift = pytz.timezone(tz).localize(datetime.datetime(2015, 1, 1)).strftime('%z')

        # форматируем для вывода в админ панели
        shift_name = "%s:%s" % (shift[:3], shift[3:])

        choices.append((shift, shift_name))

    # сортируем и возвращаем список кортежей
    return sorted(set(choices), key=lambda k: int(k[0]))


def get_minutes(time_start, time_end, force_positive_or_zero=True):
    """
        Расчёт количество минут
    :param time_start: datetime.time - начало
    :param time_end: datetime.time - конец
    :param force_positive_or_zero: bool - возвращать 0 в случае отрицательного результата
    :return: float
    """
    today = datetime.date.today()
    minutes = (datetime.datetime.combine(today, time_end) - datetime.datetime.combine(today, time_start)).total_seconds()/60
    if force_positive_or_zero:
        return minutes if minutes > 0 else 0
    else:
        return minutes


def make_summary_entry(cost, time_from, time_to, price_per_minute):
    """
        Создаёт строку для сводки
    :param cost: float - стоимость
    :param time_from: datetime.date
    :param time_to: datetime.date
    :param price_per_minute: float - цена в мин
    :return:
    """
    if cost > 0:
        return u"Начислено %s Р. в период с %s по %s по цене %s Р в мин. \n" % (cost,time_from,time_to, price_per_minute)
    else:
        return u""
