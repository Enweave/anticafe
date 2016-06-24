# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from cafe.models import RatePeriod, Cafe
from cafe.utils import get_input_date_format


class RatePeriodForm(forms.ModelForm):
    """
        форма для модели "цена в периоде".
        в методе clean реализуются дополнительные проверки (см. текст ошибок)
    """
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
                    # если форма содержит экземпляр RatePeriod - исключаем его из проверки
                    if self.instance.id:
                        existing_periods = rate.get_periods().exclude(id=self.instance.id)
                    else:
                        existing_periods = rate.get_periods()
                    for p in existing_periods:
                        # здесь проверяем, чтобы диапазон добавляемой/изменяемой RatePeriod
                        # не пересёкся с диапазонами уже существующих
                        if p.time_start < end and p.time_end > start:
                            self.add_error(None, mark_safe(
                                           u"Выбранный временной промежуток [%s|%s] <br>"
                                           u"пересекается с промежутком %s ! <br>"
                                           u"Задайте другое время, пожалуйтса."
                                           % (start, end, p)))
                            break
        return self.cleaned_data


def get_cafe_options():
    return Cafe.objects.all().values_list("id", "name")


class ReportForm(forms.Form):
    """
        Форма для запроса отчёта
    """
    cafe = forms.ChoiceField(
        choices=get_cafe_options,
        label=u"Кафе"
    )

    date_from = forms.DateField(
        widget=forms.DateInput(),
        label=u"от",
        input_formats=[get_input_date_format()]
    )

    date_to = forms.DateField(
        widget=forms.DateInput(),
        label=u"до",
        input_formats=[get_input_date_format()]
    )

    def clean(self):
        start = self.cleaned_data.get('date_from', "")
        end = self.cleaned_data.get('date_to', "")
        if start and end:
            if start > end:
                self.add_error(None, mark_safe(
                               u"Значение 'от' не может быть больше значения 'до'"))
        return self.cleaned_data