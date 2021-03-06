from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command # вызывает команду из кода например test mainapp

from mainapp.models import ProductCategory, Product


class TestMainappSmoke(TestCase): # smoke_test запустить что-то и посмотреть пойдет ли дым
    def setUp(self) -> None:
        call_command('flush', '--noinput') # чистит базу данных
        call_command('loaddata', 'test_db.json')
        self.client = Client()


    def test_mainapp_urls(self):
        response = self.client.get('/') # попадает все что сервер ответит на запрос GET
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product_detail/{product.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'orderapp', 'basketapp')



# Create your tests here.
