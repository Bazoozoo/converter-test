from django.contrib import admin
from models import CurrencyRate, CurrencyInfo


class CurrencyInfoAdmin(admin.ModelAdmin):
    ordering = ['code']
    list_display = ['name', 'code']


class CurrencyRateAdmin(admin.ModelAdmin):
    model = CurrencyRate
    list_display = ['currency_code', 'rate', 'currency_name']

    def currency_code(self, obj):
        return obj.info.code
    currency_code.admin_order_field = 'info__code'
    currency_code.short_description = 'Currency code'

    def currency_name(self, obj):
        return obj.info.name
    currency_name.admin_order_field = 'info__name'
    currency_name.short_description = 'Full currency name'


admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(CurrencyInfo, CurrencyInfoAdmin)
