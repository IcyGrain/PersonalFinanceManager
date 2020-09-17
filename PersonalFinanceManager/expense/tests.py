from django.test import TestCase, Client

from budget.models import *
from .models import *
import json
import django.utils.timezone as timezone
from datetime import timedelta


# Create your tests here.


class ExpenseTest(TestCase):

    def setUp(self):
        Category.objects.create(category="jia")
        Category.objects.create(category="yi")
        SubCategory.objects.create(category=Category.objects.get(id=1), sub_category="zi")
        SubCategory.objects.create(category=Category.objects.get(id=2), sub_category="chou")
        Account.objects.create(name="test1", account_type="saving", currency="CHY", balance=1000)
        Account.objects.create(name="test2", account_type="checking", currency="CHY", balance=1000)
        # Budget.objects.create(amount="1000", category=SubCategory.objects.get(id=1), budget_type="fixed",
        #                       start_date=timezone.now().strftime("%Y-%m-%d"),
        #                       end_date=(timezone.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
        # Budget.objects.create(amount="1000", category=SubCategory.objects.get(id=2), budget_type="fixed",
        #                       start_date=timezone.now().strftime("%Y-%m-%d"),
        #                       end_date=(timezone.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
        Expense.objects.create(amount="1000", category=SubCategory.objects.get(id=1), account=Account.objects.get(id=1),
                               payee='debt', note='For test')
        Expense.objects.create(amount="1000", category=SubCategory.objects.get(id=2), account=Account.objects.get(id=2),
                               payee='debt', note='For test')

    def test_list_expense(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.get("/expense/list_expense/")

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = [{'id': 1, 'amount': '1000.00', 'date': '2020-09-17',
                   'category': {'id': 1, 'category': {'id': 1, 'category': 'jia'}, 'sub_category': 'zi'},
                   'account': {'id': 1, 'name': 'test1', 'account_type': 'saving', 'currency': 'CHY',
                               'balance': '1000.00'}, 'payee': 'debt', 'note': 'For test'},
                  {'id': 2, 'amount': '1000.00', 'date': '2020-09-17',
                   'category': {'id': 2, 'category': {'id': 2, 'category': 'yi'}, 'sub_category': 'chou'},
                   'account': {'id': 2, 'name': 'test2', 'account_type': 'checking', 'currency': 'CHY',
                               'balance': '1000.00'}, 'payee': 'debt', 'note': 'For test'}]
        self.assertEqual(result, expect)

    def test_create_expense(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/expense/create_expense/",
                               json.dumps({'amount': 1000, 'date': timezone.now().strftime("%Y-%m-%d"),
                                           'category': 1, 'account': 2, 'payee': "debt",
                                           'note': "For create test"}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)

        expense = Expense.objects.filter(id=3, category=SubCategory.objects.get(id=1),
                                         account=Account.objects.get(id=2),
                                         note="For create test")
        self.assertTrue(expense.exists())

    def test_delete_expense(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/expense/delete_expense/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        expense = Expense.objects.filter(id=1)
        self.assertFalse(expense.exists())

    def test_update_expense(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/expense/update_expense/",
                               json.dumps({'id': 1, 'amount': 1000, 'date': timezone.now().strftime("%Y-%m-%d"),
                                           'category': 1, 'account': 1, 'payee': "debt", 'note': "For update test"}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)

        expense = Expense.objects.filter(id=1, note="For test")
        self.assertFalse(expense.exists())
        expense = Expense.objects.filter(id=1, note="For update test")
        self.assertTrue(expense.exists())

    def test_get_expense(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/expense/get_expense/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = [{'id': 1, 'amount': '1000.00', 'date': '2020-09-17',
                   'category': {'id': 1, 'category': {'id': 1, 'category': 'jia'}, 'sub_category': 'zi'},
                   'account': {'id': 1, 'name': 'test1', 'account_type': 'saving', 'currency': 'CHY',
                               'balance': '1000.00'},
                   'payee': 'debt', 'note': 'For test'}]
        self.assertEqual(result, expect)
