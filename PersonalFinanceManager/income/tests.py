from django.test import TestCase, Client
from .models import *
import json
import django.utils.timezone as timezone
# Create your tests here.


class IncomeTest(TestCase):

    def setUp(self):
        Account.objects.create(name="test1", account_type="saving", currency="CHY", balance=1000)
        Account.objects.create(name="test2", account_type="checking", currency="CHY", balance=1000)
        Income.objects.create(amount="1000", account=Account.objects.get(id=1), source="payment", note="For test")
        Income.objects.create(amount="1000", account=Account.objects.get(id=2), source="interest", note="For test")

    def test_list_income(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.get("/income/list_income/")

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = [{'id': 1, 'amount': '1000.00', 'date': '2020-09-17', 'account': {'id': 1, 'name': 'test1', 'account_type': 'saving', 'currency': 'CHY', 'balance': '1000.00'}, 'source': 'payment', 'note': 'For test'}, {'id'
: 2, 'amount': '1000.00', 'date': '2020-09-17', 'account': {'id': 2, 'name': 'test2', 'account_type': 'checking', 'currency': 'CHY', 'balance': '1000.00'}, 'source': 'interest', 'note': 'For test'}]
        self.assertEqual(result, expect)

    def test_create_income(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/income/create_income/",
                               json.dumps({'amount': 1000, 'account': 1, 'date': timezone.now().strftime("%Y-%m-%d"),
                                           'source': 'payment', 'note': 'For create test'}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)

        income = Income.objects.filter(amount=1000, account=Account.objects.get(id=1), source="payment", note="For create test")
        self.assertTrue(income.exists())

    def test_delete_income(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/income/delete_income/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        income = Income.objects.filter(id=1)
        self.assertFalse(income.exists())

    def test_update_income(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/income/update_income/",
                               json.dumps({'id': 1, 'amount': '1000.00', 'date': timezone.now().strftime("%Y-%m-%d"),
                                           'account': 1, "source": "payment", "note": "For update test"}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)

        income = Income.objects.filter(id=1, note="For test")
        self.assertFalse(income.exists())
        income = Income.objects.filter(id=1, note="For update test")
        self.assertTrue(income.exists())

    def test_get_income(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/income/get_income/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = {'id': 1, 'amount': '1000.00', 'date': '2020-09-17', 'account': 1, 'source': 'payment', 'note': 'For test'}
        self.assertEqual(result, expect)
