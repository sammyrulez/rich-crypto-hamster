from django.test import TestCase
from exchange.forms import OperationForm


class OperationFormTest(TestCase):

    def test_is_valid(self):
        opForm = OperationForm()
        opForm.amount = 10
        self.assertTrue(opForm.is_valid())
        opForm.amount = -9
        self.assertFalse(opForm.is_valid())
