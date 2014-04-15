from django.contrib.auth.models import User
from django.db import models


class Balance(models.Model):
    owner = models.ForeignKey(User)
    current_value = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return "%s owns %s bitcoins" % (self.owner.username,str(self.current_value))


class Currency(models.Model):
    name = models.CharField(max_length=3)
    base_value = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name


class ExchangeRatio(models.Model):
    ratio = models.DecimalField(decimal_places=2, max_digits=12)
    currency = models.ForeignKey(Currency)

    def __str__(self):
        return "One Bitcoin values %d %s" % (self.currentRatio, self.currency)
