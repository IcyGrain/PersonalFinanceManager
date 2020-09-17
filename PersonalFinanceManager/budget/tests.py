from django.test import TestCase, Client
from .models import *
import json
import django.utils.timezone as timezone
from datetime import timedelta


# Create your tests here.


class BudgetTest(TestCase):

    def setUp(self):
        Category.objects.create(category="jia")
        Category.objects.create(category="yi")
        SubCategory.objects.create(category=Category.objects.get(id=1), sub_category="zi")
        SubCategory.objects.create(category=Category.objects.get(id=2), sub_category="chou")
        Budget.objects.create(amount="1000", category=SubCategory.objects.get(id=1), budget_type="fixed",
                              start_date=timezone.now().strftime("%Y-%m-%d"),
                              end_date=(timezone.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
        Budget.objects.create(amount="1000", category=SubCategory.objects.get(id=2), budget_type="fixed",
                              start_date=timezone.now().strftime("%Y-%m-%d"),
                              end_date=(timezone.now() + timedelta(days=30)).strftime("%Y-%m-%d"))

    def test_list_budget(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.get("/budget/list_budget/")

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = [{'id': 1, 'amount': '1000.00', 'date': '2020-09-17',
                   'category': {'id': 1, 'category': {'id': 1, 'category': 'jia'}, 'sub_category': 'zi'},
                   'budget_type': 'fixed', 'start_date': '2020-09-17', 'end_date': '2020-10-17'},
                  {'id': 2, 'amount': '1000.00', 'date': '2020-09-17',
                   'category': {'id': 2, 'category': {'id': 2, 'category': 'yi'}, 'sub_category': 'chou'},
                   'budget_type': 'fixed', 'start_date': '2020-09-17', 'end_date': '2020-10-17'}]
        self.assertEqual(result, expect)

    def test_create_budget(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/budget/create_budget/",
                               json.dumps({'amount': 1000, 'category': 1, 'date': timezone.now().strftime("%Y-%m-%d"),
                                           'budget_type': 'fixed', "start_date": timezone.now().strftime("%Y-%m-%d"),
                                           "end_date": (timezone.now() + timedelta(days=30)).strftime("%Y-%m-%d")}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)

        budget = Budget.objects.filter(id=3, amount=1000, category=SubCategory.objects.get(id=1), budget_type="fixed")
        self.assertTrue(budget.exists())

    def test_delete_budget(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/budget/delete_budget/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        budget = Budget.objects.filter(id=1)
        self.assertFalse(budget.exists())

    def test_update_budget(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/budget/update_budget/",
                               json.dumps(
                                   {'id': 1, 'amount': 2000, 'category': 1, 'date': timezone.now().strftime("%Y-%m-%d"),
                                    'budget_type': 'float', "start_date": timezone.now().strftime("%Y-%m-%d"),
                                    "end_date": (timezone.now() + timedelta(days=30)).strftime("%Y-%m-%d")}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)

        budget = Budget.objects.filter(id=1, budget_type="fixed")
        self.assertFalse(budget.exists())
        budget = Budget.objects.filter(id=1, budget_type="float")
        self.assertTrue(budget.exists())

    def test_get_budget(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/budget/get_budget/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = {'id': 1, 'amount': '1000.00', 'date': '2020-09-17', 'category': 1, 'budget_type': 'fixed',
                  'start_date': '2020-09-17', 'end_date': '2020-10-17'}
        self.assertEqual(result, expect)
