from django.contrib import admin
from django.urls import path
from core.views import whatsapp_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/', whatsapp_webhook, name='webhook'),
]
