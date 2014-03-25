from django import forms
from money.contrib.django.forms.fields import MoneyField


class OperationForm(forms.Form):

    amount = forms.IntegerField()

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if not data or data < 0:
            raise forms.ValidationError("Invalid amount")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
