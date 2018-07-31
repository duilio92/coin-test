# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
# from snippets.views import SnippetViewSet, UserViewSet, api_root
# from rest_framework import renderers
from rest_framework.routers import DefaultRouter
# from rest_framework.urlpatterns import format_suffix_patterns
router = DefaultRouter()
router.register(
    r'transactions',
    views.CustomTransactionViewSet,
    base_name='transaction')


urlpatterns = [
    url(r'^', include(router.urls)),
]
