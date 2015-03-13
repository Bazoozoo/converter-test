# -*- coding: utf-8 -*-
import datetime
import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from celery import task
from celery.utils.log import get_task_logger
from aggregator.models import CurrencyRate, CurrencyInfo

logger = get_task_logger(__name__)
APP_ID = getattr(settings, 'OPENEXCHANGERATES_APP_ID', None)
API_URL = getattr(settings, 'OPENEXCHANGERATES_API_URL', None)

if APP_ID is None:
        raise ImproperlyConfigured("App ID not found. Did you define it in settings.py?(OPENEXCHANGERATES_APP_ID)")
if API_URL is None:
    raise ImproperlyConfigured("API Url not found. Did you define it in settings.py?(OPENEXCHANGERATES_API_URL)")


@task(bind=True, max_retries=3)
def get_currency_rates(self):
    logger.info("fetching data")
    request_parameters = {
        'app_id': APP_ID,
    }
    try:
        r = requests.get(API_URL, params=request_parameters)
    except requests.ConnectionError as e:
        raise self.retry(exc=e, countdown=5)
    currency_data = r.json()
    for code, rate in currency_data['rates'].items():
        curr_info = CurrencyInfo.objects.get(code=code)
        try:
            curr_rate = CurrencyRate.objects.get(info=curr_info)
        except CurrencyRate.DoesNotExist:
            curr_rate = CurrencyRate(info=curr_info)
        curr_rate.rate = rate
        curr_rate.last_updated = datetime.datetime.fromtimestamp(currency_data["timestamp"])
        curr_rate.save()
