# -*- coding: utf-8 -*-
from django import forms
from aggregator.models import CurrencyInfo


class ConvertCurrencyForm(forms.Form):
    amount = forms.FloatField()
    currency_from = forms.ModelChoiceField(CurrencyInfo.objects.all())
    currency_to = forms.ModelChoiceField(CurrencyInfo.objects.all())