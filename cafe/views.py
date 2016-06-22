# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from cafe.models import Cafe, Table


def cafe_mixin(cafe, context):
    context.update({
        "item": cafe,
        "breadcrumbs": cafe.get_breadcrumbs()
    })
    return context


def cafe_detail(request, pk):
    cafe = get_object_or_404(Cafe, pk=pk)
    return render(
        request,
        "cafe/cafe_detail.html",
        cafe_mixin(cafe, {})
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
    if success:
        messages.success(request, u"<p>%s освобождён</p>" % table.name, extra_tags="success")
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