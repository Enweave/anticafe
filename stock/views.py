# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from cafe.models import Cafe
from stock.forms import SpentStockItemForm, StockItemFieldset
from stock.models import StockItem
from django.http import JsonResponse, HttpResponseRedirect


def get_stock_items(request, cafe_id):
    if request.is_ajax():
        choices = StockItem.objects.filter(cafe=Cafe.objects.get(id=cafe_id), active=True).values_list("id", "name")
        form = StockItemFieldset(choices)
        item_name = u'Продукт'
        html = render_to_string("stock/templatetags/stock_fieldset.html", locals())
        return JsonResponse({"html": html})
    return HttpResponseRedirect("/")


def edit_stock(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)

    breadcrumbs = cafe.get_breadcrumbs()
    breadcrumbs.append({"title": u"склад"})

    stock_items = StockItem.objects.filter(cafe=cafe, active=True)

    form = SpentStockItemForm()
    if request.POST:
        # Основные поля поставки фиксируем с помощью объекта формы
        form = SpentStockItemForm(request.POST)
        if form.is_valid():
            # consumables = []
            # for i, consumble_type in enumerate(request.POST.getlist("consumable_type", ())):
            #     consumables.append({"type": consumble_type, "count": int(request.POST.getlist("consumable_count")[i])})
            #
            # for consumable in consumables:
            #
            #     new_supplied_consumable = SuppliedConsumable(
            #         supply=new_supply,
            #         consumable_type=ConsumableType.objects.get(id=consumable["type"]),
            #         consumable_count=consumable["count"]
            #     )
            #     new_supplied_consumable.save()
            messages.success(request, u"<p>Изменение успешно проведено</p>", extra_tags="success")

            return HttpResponseRedirect(reverse('stock:edit-stock', kwargs={"cafe_id": cafe_id}))
    return render(request, "stock/stock_detail.html", {
        "cafe": cafe,
        "breadcrumbs": breadcrumbs,
        "stock_items": stock_items,
        "form": form
    })
