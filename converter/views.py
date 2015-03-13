import json
from django.contrib import messages
from django.core.cache import cache
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from aggregator.models import CurrencyRate
from converter.forms import ConvertCurrencyForm


CACHE_TIMEOUT = 30 * 60


class UnknownCurrency(Exception):
    pass


def home(request):
    if request.method == "GET":
        form = ConvertCurrencyForm()
        return render(request, "index.html", {'form': form})
    elif request.method == "POST":
        form = ConvertCurrencyForm(request.POST)
        if form.is_valid():
            return redirect('page_convert',
                            amount=form.cleaned_data['amount'],
                            code_from=form.cleaned_data['currency_from'].code,
                            code_to=form.cleaned_data['currency_to'].code,
                            response_type='html')
        return render(request, "index.html", {'form': form})


def convert(request, amount, code_from, code_to, response_type):
    response_type = response_type.lower()
    response_data = {}
    try:
        result = __convert_currency(amount, code_from, code_to)
        response_data['success'] = True
        response_data['result'] = result
    except UnknownCurrency as e:
        response_data['success'] = False
        response_data['error'] = str(e)
    if response_type == 'html':
        if response_data['success']:
            response_data['amount'] = amount
            response_data['currency_from'] = code_from.upper()
            response_data['currency_to'] = code_to.upper()
            return render(request, "convert.html", response_data)
        else:
            messages.error(request, response_data['error'])
            return redirect('page_home')
    elif response_type == 'json':
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    elif response_type == 'text':
        if response_data['success']:
            return HttpResponse(response_data['result'], content_type='text/plain')
        else:
            return HttpResponse(response_data['error'], content_type='text/plain')


def __convert_currency(amount, code_from, code_to):
    try:
        rate_from = __get_currency_rate(code_from)
    except UnknownCurrency as exc:
        exc.message = "Unknown source currency code: %s" % code_from
        raise exc
    try:
        rate_to = __get_currency_rate(code_to)
    except UnknownCurrency as exc:
        exc.message = "Unknown target currency code: %s" % code_to
        raise exc
    result = float(amount) * (rate_to / rate_from)
    return result


def __get_currency_rate(currency_code):
    currency_code = currency_code.upper()
    rate = cache.get(currency_code)
    if rate is None:
        try:
            rate = CurrencyRate.objects.get(info__code=currency_code).rate
            cache.set(currency_code, rate, CACHE_TIMEOUT)
        except CurrencyRate.DoesNotExist:
            raise UnknownCurrency
    return rate

