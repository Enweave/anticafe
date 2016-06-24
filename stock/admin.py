from django import forms
from django.contrib import admin

# Register your models here.

from models import StockItem, SpentStockItem, Unit


class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "entry", "active")
    list_filter = ("active",)

admin.site.register(Unit, UnitAdmin)


class StockItemAdmin(admin.ModelAdmin):
    list_display = ("name", "cafe", "quantity", "active")
    list_filter = ("cafe", "active")

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.exclude = ('quantity',)
        else:
            self.exclude = ()
        return super(StockItemAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(StockItem, StockItemAdmin)

class SpentStockItemAdmin(admin.ModelAdmin):
    list_display = ("stock_item", "date", "quantity")
    list_filter = ("stock_item",)

admin.site.register(SpentStockItem, SpentStockItemAdmin)