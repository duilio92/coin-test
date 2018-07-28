"""ripiotest URL Configuration."""
from django.conf.urls import url, include
from django.contrib import admin
from transactions.urls import router as transactionrouter
from coins.urls import router as coinrouter
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.registry.extend(coinrouter.registry)
router.registry.extend(transactionrouter.registry)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls, namespace='api')),
    #url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^coins/', include('coins.urls', namespace='coins')),
    #url(r'^transactions/', include('transactions.urls', namespace='transactions')),
]
