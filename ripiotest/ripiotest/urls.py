"""ripiotest URL Configuration."""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^coins/', include('coins.urls', namespace='coins')),
    url(r'^transactions/', include('transactions.urls', namespace='coins')),
]
