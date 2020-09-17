from django.forms import model_to_dict
from django.test import TestCase, Client
from .models import *
import json
# Create your tests here.


class CategoryTest(TestCase):

    def setUp(self):
        Category.objects.create(category="jia")
        Category.objects.create(category="yi")
        SubCategory.objects.create(category=Category.objects.get(id=1), sub_category="zi")
        SubCategory.objects.create(category=Category.objects.get(id=1), sub_category="chou")
        SubCategory.objects.create(category=Category.objects.get(id=2), sub_category="yin")
        SubCategory.objects.create(category=Category.objects.get(id=2), sub_category="mao")

    def test_list_category(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.get("/category/list_category/")

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = list(Category.objects.all().values())
        self.assertEqual(result, expect)

    def test_list_sub_category(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/category/list_sub_category/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = list(SubCategory.objects.filter(category=1).values())
        self.assertEqual(result, expect)

    def test_create_category(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/category/create_category/", {"category": "test"})

        self.assertEqual(response.status_code, 200)

        category = Category.objects.filter(category="test")
        self.assertTrue(category.exists())

    def test_create_sub_category(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/category/create_sub_category/", json.dumps({"category": 1, "sub_category": "test"}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)

        sub_category = SubCategory.objects.filter(sub_category="test")
        self.assertTrue(sub_category.exists())

        category = Category.objects.get(id=1)
        self.assertEqual(sub_category.first().category, category)

    def test_delete_category(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')

        sub_category = SubCategory.objects.filter(category=Category.objects.get(id=1))

        response = client.post("/category/delete_category/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        category = Category.objects.filter(id=1)
        self.assertFalse(category.exists())

        self.assertFalse(sub_category.exists())

    def test_delete_sub_category(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/category/delete_sub_category/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        sub_category = SubCategory.objects.filter(id=1)
        self.assertFalse(sub_category.exists())

    def test_update_category(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/category/update_category/", {"id": 1, "category": "test"})

        self.assertEqual(response.status_code, 200)

        category = Category.objects.filter(category="jia")
        self.assertFalse(category.exists())
        category = Category.objects.filter(category="test")
        self.assertTrue(category.exists())

    def test_update_sub_category(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/category/update_sub_category/",
                               json.dumps({"id": 1, "category": 2, "sub_category": "test"}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)

        sub_category = SubCategory.objects.filter(sub_category="zi")
        self.assertFalse(sub_category.exists())
        sub_category = SubCategory.objects.filter(sub_category="test")
        self.assertTrue(sub_category.exists())

        category = Category.objects.get(id=2)
        self.assertEqual(sub_category.first().category, category)

    def test_get_category(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/category/get_category/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = model_to_dict(Category.objects.get(id=1))
        self.assertEqual(result, expect)

    def test_get_sub_category(self):
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.post("/category/get_sub_category/", {"id": 1})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)['result']
        expect = model_to_dict(SubCategory.objects.get(id=1))
        self.assertEqual(result, expect)
