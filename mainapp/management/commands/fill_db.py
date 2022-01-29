import json
import os

from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

JSON_PATH = 'mainapp/jsons'


def load_from_json(file_nm):
    """
    """
    with open(os.path.join(JSON_PATH, file_nm + '.json'), 'r', encoding='utf-8') as ld_file:
        return json.load(ld_file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()
        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_id = product['category_id']
            _category = ProductCategory.objects.get(pk=category_id)
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        ShopUser.objects.create_superuser(username='admin', email="none@none.com", password='123', age=30)
