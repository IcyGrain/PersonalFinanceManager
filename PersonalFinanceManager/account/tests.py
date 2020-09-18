from django.forms import model_to_dict
from django.test import TestCase, Client
from .models import *
from expense.models import *
from income.models import *
import json


# Create your tests here.


class AccountTest(TestCase):

    def setUp(self):
        Account.objects.create(name="test1", account_type="saving", currency="CNY", balance=1000)
        Account.objects.create(name="test2", account_type="checking", currency="CNY", balance=1000)
        Category.objects.create(category="jia")
        SubCategory.objects.create(category=Category.objects.get(id=1), sub_category="zi")
        Expense.objects.create(amount="1000", category=SubCategory.objects.get(id=1), account=Account.objects.get(id=1),
                               payee='debt', note='For test')
        Income.objects.create(amount="1000", account=Account.objects.get(id=1), source="payment", note="For test")

    def test_list_transaction(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/account/list_transaction/", {'id': 1})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = {'expense': [{'id': 1, 'amount': '1000.00', 'date': timezone.now().strftime("%Y-%m-%d"),
                               'category': {'id': 1, 'category': {'id': 1, 'category': 'jia'}, 'sub_category': 'zi'},
                               'account': {'id': 1, 'name': 'test1', 'account_type': 'saving', 'currency': 'CNY',
                                           'balance': '1000.00'}, 'payee': 'debt', 'note': 'For test'}], 'income': [
            {'id': 1, 'amount': '1000.00', 'date': timezone.now().strftime("%Y-%m-%d"),
             'account': {'id': 1, 'name': 'test1', 'account_type': 'saving', 'currency': 'CNY', 'balance': '1000.00'},
             'source': 'payment', 'note': 'For test'}]}
        self.assertEqual(result, expect)

    def test_list_account(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.get("/account/list_account/")

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = [{'id': 1, 'name': 'test1', 'account_type': 'saving', 'currency': 'CNY', 'balance': '1000.00'},
                  {'id': 2, 'name': 'test2', 'account_type': 'checking', 'currency': 'CNY', 'balance': '1000.00'}]
        self.assertEqual(result, expect)

    def test_create_account(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/account/create_account/",
                               {'name': 'test3', 'account_type': 'saving', 'currency': 'CNY', 'balance': '1000.00'})

        self.assertEqual(response.status_code, 200)

        account = Account.objects.filter(name="test3")
        self.assertTrue(account.exists())

    def test_delete_account(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/account/delete_account/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        account = Account.objects.filter(id=1)
        self.assertFalse(account.exists())

    def test_update_account(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/account/update_account/",
                               {"id": 1, 'name': 'test3', 'account_type': 'saving', 'currency': 'CNY',
                                'balance': '1000.00'})

        self.assertEqual(response.status_code, 200)

        account = Account.objects.filter(name="test1")
        self.assertFalse(account.exists())
        account = Account.objects.filter(name="test3")
        self.assertTrue(account.exists())

    def test_get_account(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/account/get_account/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = {'id': 1, 'name': 'test1', 'account_type': 'saving', 'currency': 'CNY', 'balance': '1000.00'}
        self.assertEqual(result, expect)
