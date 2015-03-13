# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'converter.views.home', name='page_home'),
    url(r'^(?P<amount>[0-9]*\.?[0-9]*)/(?P<code_from>(?i)[a-zA-Z]{3})/to/(?P<code_to>(?i)[a-zA-Z]{3})/in/(?P<response_type>(?i)text|json|html)/$',
        'converter.views.convert', name='page_convert'),
)
