# -*- coding: utf-8 -*-
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'coins', views.CoinViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'coinaccounts', views.CoinAccountViewSet)
