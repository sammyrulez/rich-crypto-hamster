from django.contrib import admin
from exchange.models import Currency, ExchangeRatio

admin.site.register(Currency)
admin.site.register(ExchangeRatio)