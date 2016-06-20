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

admin.site.register(StockItem, StockItemAdmin)

class SpentStockItemAdmin(admin.ModelAdmin):
    list_display = ("stock_item", "date", "quantity")
    list_filter = ("stock_item",)

admin.site.register(SpentStockItem, SpentStockItemAdmin)