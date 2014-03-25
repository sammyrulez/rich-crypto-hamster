from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from exchange.forms import OperationForm



class OperationFormTest(TestCase):

    def test_is_valid(self):
        opForm = OperationForm({'amount': 10})
        self.assertTrue(opForm.is_valid())
        opForm = OperationForm({'amount': -9})
        self.assertFalse(opForm.is_valid())


class DepositViewTest(TestCase):

    def test_form_display(self):
        c = Client()
        url = reverse('deposit')
        response = c.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTrue("submit" in response.content)
        self.assertTrue("amount" in response.content)

    def test_form_submit(self):
        c = Client()
        url = reverse('deposit')
        response = c.post(url, data={'amount':10})
        self.assertEquals(302, response.status_code)

    def test_form_validation(self):
        c = Client()
        url = reverse('deposit')
        response = c.post(url)
        self.assertEquals(200, response.status_code)

        self.assertTrue("submit" in response.content)
        self.assertTrue("amount" in response.content)
        self.assertTrue("This field is required." in response.content)

        response = c.post(url,data={'amount':-9})
        self.assertEquals(200,response.status_code)
        self.assertTrue("Invalid amount" in response.content)
