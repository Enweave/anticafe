# -*- coding: utf-8 -*-
from django.utils import timezone
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