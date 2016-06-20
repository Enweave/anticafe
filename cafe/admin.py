# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.

from models import Cafe, Rate, RatePeriod, Table, Visit


class CafeAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Cafe, CafeAdmin)


class RateAdmin(admin.ModelAdmin):
    list_display = ('name', 'cafe', 'list_periods')

    def list_periods(self, obj):
        return reduce(lambda a, b: a+u"%s<br>, " % b, [i.__unicode__() for i in obj.get_periods()], u"")[:-2]

    list_periods.short_description = u"Цены в минуту"
    list_periods.allow_tags = True

admin.site.register(Rate, RateAdmin)


class RatePeriodAdmin(admin.ModelAdmin):
    list_display = ("get_title",)

    def get_title(self, obj):
        return obj.__unicode__()

    get_title.short_description = u"Название"

admin.site.register(RatePeriod, RatePeriodAdmin)


class TableAdmin(admin.ModelAdmin):
    list_display = ("name", "cafe", "rate", "active")
    list_filter = ("active",)

admin.site.register(Table, TableAdmin)


class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "table", "active")
    list_filter = ("table", "active")

admin.site.register(Visit, VisitAdmin)