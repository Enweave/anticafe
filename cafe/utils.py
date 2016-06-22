# -*- coding: utf-8 -*-

import datetime
import pytz


def get_timezone_choices():
    choices = []
    for tz in pytz.common_timezones:
        shift = pytz.timezone(tz).localize(datetime.datetime(2015, 1, 1)).strftime('%z')
        shift_name = "%s:%s" % (shift[:3], shift[3:])
        choices.append((shift, shift_name))
    return sorted(set(choices), key=lambda k: int(k[0]))


def get_minutes(time_start, time_end, force_positive_or_zero=True):
    today = datetime.date.today()
    minutes = (datetime.datetime.combine(today, time_end) - datetime.datetime.combine(today, time_start)).total_seconds()/60
    if force_positive_or_zero:
        return minutes if minutes > 0 else 0
    else:
        return minutes


def make_summary_entry(cost, time_from, time_to, price_per_minute):
    if cost > 0:
        return u"Начислено %s Р. в период с %s по %s по цене %s Р в мин. \n" % (cost,time_from,time_to, price_per_minute)
    else:
        return u""
