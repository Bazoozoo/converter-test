from django.db import models


class CurrencyInfo(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=3)

    def __unicode__(self):
        return u'%s' % self.code


class CurrencyRate(models.Model):
    rate = models.FloatField()
    name = models.ForeignKey('CurrencyInfo')
    last_updated = models.DateTimeField()

    def __unicode__(self):
        return u'%s(%s): %s' % (self.name.code.upper(), self.name.name, self.rate)
