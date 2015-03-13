from django.db import models


class CurrencyInfo(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=3)

    def __unicode__(self):
        return u'%s(%s)' % (self.name, self.code)


class CurrencyRate(models.Model):
    rate = models.FloatField()
    info = models.ForeignKey('CurrencyInfo')
    last_updated = models.DateTimeField()

    def __unicode__(self):
        return u'%s: %s' % (self.info, self.rate)
