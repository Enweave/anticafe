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

    # def has_delete_permission(self, request, obj=None):
    #     return False

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
    readonly_fields = ("stock_item", "date", "quantity", "current_quantity")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
admin.site.register(SpentStockItem, SpentStockItemAdmin)