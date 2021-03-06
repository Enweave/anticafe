# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import floatformat

from cafe.forms import ReportForm
from cafe.models import Cafe, Table, Visit


def cafe_detail(request, pk):
    cafe = get_object_or_404(Cafe, pk=pk)
    return render(
        request,
        "cafe/cafe_detail.html",
        {
            "item": cafe,
            "breadcrumbs": cafe.get_breadcrumbs()
        }
    )


def activate_table(request, table):
    if table.get_active_visit():
        success = False
    else:
        success = table.make_new_visit()
    if success:
        messages.success(request, u"<p>%s занят</p>" % table.name, extra_tags="success")
    else:
        messages.success(request, u"<p>Произошла ошибка!<br> %s уже занят</p>" % table.name, extra_tags="danger")

def deactivate_table(request, table):
    if table.get_active_visit():
        success = table.end_active_visit_and_calculate()
    else:
        success = False
    if success != False:
        messages.success(request,
            u"<p>%s освобождён<p><p> К ОПЛАТЕ: %s Р.</p>" %
            (table.name, intcomma(floatformat(success, 0))),
            extra_tags="success"
        )
    else:
        messages.success(request, u"<p>Произошла ошибка!<br> %s не был занят</p>" % table.name, extra_tags="danger")


def cancel_table(request, table):
    if table.get_active_visit():
        success = table.cancel_visit()
    else:
        success = False
    if success:
        messages.success(request, u"<p>%s освобождён</p>" % table.name, extra_tags="success")
    else:
        messages.success(request, u"<p>Произошла ошибка!<br> %s не был занят</p>" % table.name, extra_tags="danger")


def empty_table_function(request, table):
    pass


def toggle_table(request, pk, key):
    table = get_object_or_404(Table, pk=pk, active=True)

    table_dispatch = {
        '0': deactivate_table,
        '1': activate_table,
        '2': cancel_table
    }

    table_dispatch.get(key, empty_table_function)(request, table)

    return redirect(reverse("cafe:cafe-detail", kwargs={"pk": table.cafe.pk}))


def reports(request):
    form = ReportForm()
    items = []
    has_report = False
    items_count = 0
    total_cost = 0
    if request.POST:
        form = ReportForm(request.POST)
        if form.is_valid():
            has_report=True
            cafes = Cafe.objects.filter(id=form.cleaned_data.get("cafe", ""))
            if cafes:
                cafe = cafes[0]
                tables = cafe.get_tables().values_list("id", flat=True)
                to = form.cleaned_data.get('date_to', "")
                if to:
                    to += datetime.timedelta(days=1)
                items = Visit.objects.filter(
                    start__gte=form.cleaned_data.get('date_from', ""),
                    start__lte=to,
                    table__id__in=tables,
                    active=False
                )
                items_count = items.count()
                total_cost = reduce(lambda a,b: a + b, [i.total_cost if i.total_cost else 0 for i in items], 0)
    return render(request,"cafe/reports_page.html", {
        "breadcrumbs": [{"title": "отчёты" }],
        "report_form": form,
        "nav_selected": 0,
        "items": items,
        "has_report": has_report,
        "items_count": items_count,
        "total_cost": total_cost
    })