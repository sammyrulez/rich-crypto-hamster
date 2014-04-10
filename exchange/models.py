from django.contrib.auth.models import User
from django.db import models


class Balance(models.Model):
    owner = models.ForeignKey(User)
    current_value = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return "%s owns %s bitcoins" % (self.owner.username,str(self.current_value))

class ExchangeRatio(models.Model):
    currentRatio = models.DecimalField(decimal_places=2, max_digits=12 )
    currency = models.CharField(max_length=3)

    def __str__(self):
        return "One Bitcoin values %d %s" % (self.currentRatio, self.currency)