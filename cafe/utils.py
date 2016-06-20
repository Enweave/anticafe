# -*- coding: utf-8 -*-

import datetime
import pytz


def get_timezone_choices(predefined=True):
    if predefined:
        choices = []
        for tz in pytz.common_timezones:
            shift = pytz.timezone(tz).localize(datetime.datetime(2015, 1, 1)).strftime('%z')
            shift_name = "%s:%s" % (shift[:3], shift[3:])
            choices.append((int(shift), shift_name))
        return sorted(set(choices), key=lambda k: int(k[0]))
    else:
        return [(-1100, '-11:00'), (-1000, '-10:00'), (-930, '-09:30'), (-900, '-09:00'), (-800, '-08:00'),
                (-700, '-07:00'), (-600, '-06:00'), (-500, '-05:00'), (-430, '-04:30'), (-400, '-04:00'),
                (-330, '-03:30'), (-300, '-03:00'), (-200, '-02:00'), (-100, '-01:00'), (0, '00:00'),
                (100, '+01:00'), (200, '+02:00'), (300, '+03:00'), (330, '+03:30'), (400, '+04:00'),
                (430, '+04:30'), (500, '+05:00'), (530, '+05:30'), (545, '+05:45'), (600, '+06:00'),
                (630, '+06:30'), (700, '+07:00'), (800, '+08:00'), (845, '+08:45'), (900, '+09:00'),
                (930, '+09:30'), (1000, '+10:00'), (1030, '+10:30'), (1100, '+11:00'), (1130, '+11:30'),
                (1200, '+12:00'), (1300, '+13:00'), (1345, '+13:45'), (1400, '+14:00')]