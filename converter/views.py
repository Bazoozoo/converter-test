import json
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from aggregator.models import CurrencyRate
from converter.forms import ConvertCurrencyForm


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
        rate_from = CurrencyRate.objects.get(name__code=code_from.upper())
    except CurrencyRate.DoesNotExist:
        raise UnknownCurrency("Unknown source currency code: %s" % code_from.upper())
    try:
        rate_to = CurrencyRate.objects.get(name__code=code_to.upper())
    except CurrencyRate.DoesNotExist:
        raise UnknownCurrency("Unknown target currency code: %s" % code_to.upper())
    result = float(amount) * (rate_to.rate / rate_from.rate)
    return result
