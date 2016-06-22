# -*- coding: utf-8 -*-

from django import template
from cafe.models import Cafe

register = template.Library()


@register.inclusion_tag("cafe/templatetags/cafe_list.html")
def cafe_list():
    items = Cafe.objects.all()
    return {"items": items }