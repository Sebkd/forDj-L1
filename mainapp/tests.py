from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command # вызывает команду из кода например test mainapp


class TestMainappSmoke(TestCase): # smoke_test запустить что-то и посмотреть пойдет ли дым
    def setUp(self) -> None:
        call_command('flush', '--noinput') # чистит базу данных
        call_command('loaddata', 'test_db.json')
        self.client = Client()


    def test_mainapp_urls(self):
        response = self.client.get('/') # попадает все что сервер ответит на запрос GET
        self.assertEqual(response.status_code, 200)



# Create your tests here.
