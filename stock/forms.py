# -*- coding: utf-8 -*-
from django.utils import timezone
from django.utils.safestring import mark_safe
from cafe.models import get_cafe_options
from cafe.utils import get_input_date_format

from models import StockItem, SpentStockItem
from django import forms


def formated_timezone_now():
    return timezone.now().strftime(get_input_date_format())


class SpentStockItemForm(forms.Form):
    """
        Основа для формы продуктов
    """
    date = forms.DateField(
        widget=forms.DateInput(),
        label=u"Дата",
        input_formats=[get_input_date_format()],
        initial=formated_timezone_now
    )


class StockItemFieldset(forms.ModelForm):
    """
        Используется для генерации полей параметров изменения количество продууктов
    """

    class Meta:
        model = SpentStockItem
        fields = ("stock_item", "quantity")

    def __init__(self, choices=(), *args, **kwargs):
        super(StockItemFieldset, self).__init__()
        self.fields['stock_item'].widget.attrs.update({"data-role": "fieldset-name-source"})
        self.fields['quantity'].label = u"на сколько изменить"
        self.fields['stock_item'].choices = choices


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