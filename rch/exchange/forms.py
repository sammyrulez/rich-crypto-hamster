from django import forms
from money.contrib.django.forms.fields import MoneyField


class OperationForm(forms.Form):

    amount = MoneyField()

    def is_valid(self):
        return self.amount > 0


