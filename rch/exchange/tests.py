from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from exchange.forms import OperationForm


class OperationFormTest(TestCase):

    def test_is_valid(self):
        opForm = OperationForm()
        opForm.amount = 10
        self.assertTrue(opForm.is_valid())
        opForm.amount = -9
        self.assertFalse(opForm.is_valid())


class DepositViewTest(TestCase):

    def test_form_display(self):

        c = Client()
        url = reverse('deposit');
        response = c.get(url)
        self.assertEquals(200,response.status_code)

