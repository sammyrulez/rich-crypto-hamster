from decimal import Decimal
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from event_sourcing.mongodb_event_storage import SOURCED_EVENTS
from exchange.forms import OperationForm
import exchange
from exchange import models
from datetime import datetime

PASSWORD = 'kabala'

TESTDUMMYUSER = 'testdummyuser'


class OperationFormTest(TestCase):

    def test_is_valid(self):
        opForm = OperationForm({'amount': 10})
        self.assertTrue(opForm.is_valid())
        opForm = OperationForm({'amount': -9})
        self.assertFalse(opForm.is_valid())


class DepositViewTest(TestCase):

    fixtures = ['auth']

    def setUp(self):
        print 'DepositViewTest'
        super(DepositViewTest, self).setUp()
        self.client = Client()
        self.client.login(username=TESTDUMMYUSER, password=PASSWORD)

    def test_auth_only(self):
        un_auth_client = Client()
        url = reverse('deposit')
        response = un_auth_client.get(url)
        self.assertEquals(302, response.status_code)

    def test_form_display(self):
        url = reverse('deposit')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTrue("submit" in response.content)
        self.assertTrue("amount" in response.content)

    def test_form_submit(self):
        url = reverse('deposit')
        response = self.client.post(url, data={'amount': 10})
        self.assertEquals(302, response.status_code)

    def test_form_validation(self):
        url = reverse('deposit')
        response = self.client .post(url)
        self.assertEquals(200, response.status_code)

        self.assertTrue("submit" in response.content)
        self.assertTrue("amount" in response.content)
        self.assertTrue("This field is required." in response.content)

        response = self.client .post(url, data={'amount': -9})
        self.assertEquals(200, response.status_code)
        self.assertTrue("Invalid amount" in response.content)


class WithdrawViewTest(TestCase):

    fixtures = ['auth']

    def setUp(self):
        super(WithdrawViewTest, self).setUp()
        self.client = Client()
        self.client.login(username=TESTDUMMYUSER, password=PASSWORD)

    def test_auth_only(self):
        un_auth_client = Client()
        url = reverse('withdraw')
        response = un_auth_client.get(url)
        self.assertEquals(302, response.status_code)

    def test_form_display(self):
        url = reverse('withdraw')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTrue("submit" in response.content)
        self.assertTrue("amount" in response.content)


class DenormalizerTest(TestCase):

    fixtures = ['auth','exchange']

    def setUp(self):
        self.collection = exchange.db[SOURCED_EVENTS]
        self.deposit_amount = 50
        self.collection.insert({'event': "deposit", 'payload':  {'user': TESTDUMMYUSER, 'amount': self.deposit_amount, 'timestamp' : datetime.now() }})
        for k in range(0, 1000):
            self.collection.insert({'event': "deposit", 'payload':  {'user': 'admin', 'amount': 20, 'timestamp' : datetime.now() }})

    def tearDown(self):
        self.collection.remove()


    def test_balance_normalization(self):
        exchange.update_balance_on_event_stored(self)
        user_data = User.objects.get(username = TESTDUMMYUSER)
        balances = models.Balance.objects.filter(owner= user_data).all()
        for balance in balances:
            self.assertEquals(self.deposit_amount,balance.current_value)

    def test_ratio_normalization(self):
        exchange.update_exchange_ratio_on_event_stored(self)
        self.assertEquals(3,models.ExchangeRatio.objects.count())
        ratios = models.ExchangeRatio.objects.all()
        for r in ratios:
            self.assertTrue(r.ratio < Decimal(1.3))

