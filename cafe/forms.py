# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from cafe.models import RatePeriod


class RatePeriodForm(forms.ModelForm):
    class Meta:
        model = RatePeriod
        fields = ("rate", "time_start", "time_end", "price")

    def clean(self):
        rate = self.cleaned_data.get('rate', "")
        if rate:
            start = self.cleaned_data.get('time_start', "")
            end = self.cleaned_data.get('time_end', "")
            if start and end:
                if start >= end:
                    self.add_error(None, u"Время окончания должно быть больше времения начала")
                else:
                    if self.instance.id:
                        existing_periods = rate.get_periods().exclude(id=self.instance.id)
                    else:
                        existing_periods = rate.get_periods()
                    for p in existing_periods:
                        if p.time_start < end and p.time_end > start:
                            self.add_error(None, mark_safe(
                                           u"Выбранный временной промежуток [%s|%s] <br>"
                                           u"пересекается с промежутком %s ! <br>"
                                           u"Задайте другое время, пожалуйтса."
                                           % (start, end, p)))
                            break
        return self.cleaned_data