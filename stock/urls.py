# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

urlpatterns = patterns('stock.views',
    url(r'^edit_stock-(?P<cafe_id>[-\d]+)/$', 'edit_stock', name='edit-stock'),
    url(r'^get_stock_items-(?P<cafe_id>[-\d]+)/$', 'get_stock_items', name='get-stock-items'),
    # url(r'^remove_supply/(?P<pk>[-\d]+)/', 'remove_supply', name="remove_supply"),
)