# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from cafe.models import Cafe
from stock.forms import SpentStockItemForm, StockItemFieldset, ReportForm
from stock.models import StockItem, SpentStockItem
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
        form = SpentStockItemForm(request.POST)
        if form.is_valid():
            spent_items = request.POST.getlist("stock_item", ())

            if spent_items:
                for i, iid in enumerate(spent_items):
                    int(request.POST.getlist("quantity")[i])
                    stock_item = stock_items.get(id=iid)
                    quantity = int(request.POST.getlist("quantity")[i])
                    new_stock_spent_item = SpentStockItem(
                        stock_item=stock_item,
                        unit=stock_item.unit,
                        quantity=int(request.POST.getlist("quantity")[i])
                    )

                    new_stock_spent_item.save()
                    stock_item.quantity += quantity
                    stock_item.save()
                messages.success(request, u"<p>Изменение успешно проведено</p>", extra_tags="success")

                return HttpResponseRedirect(reverse('stock:edit-stock', kwargs={"cafe_id": cafe_id}))
    return render(request, "stock/stock_detail.html", {
        "cafe": cafe,
        "breadcrumbs": breadcrumbs,
        "stock_items": stock_items,
        "form": form
    })


def stock_reports(request):
    form = ReportForm()
    has_report = False

    if request.POST:
        form = ReportForm(request.POST)

    return render(request, "stock/report.html", {
        "breadcrumbs": [{"title": "отчёты (склады)" }],
        "report_form": form,
        "nav_selected": 1,
        "has_report": has_report,
    })
