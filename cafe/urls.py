# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

urlpatterns = patterns('cafe.views',
    url(r'^cafe-(?P<pk>[-\d]+)/$', 'cafe_detail', name='cafe-detail'),
    url(r'^toggle_table-(?P<pk>[-\d]+)/(?P<key>[-\d]+)/$', 'toggle_table', name='toggle-table'),
    # url(r'^remove_supply/(?P<pk>[-\d]+)/', 'remove_supply', name="remove_supply"),
)