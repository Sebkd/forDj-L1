from datetime import timedelta

from django.core.management.base import BaseCommand

# скидки
from django.db.models import Q, F


class Command(BaseCommand):
    def handle(self, *args, **options):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12) # временная дельта
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired = 0.05

        # Product.objects.filter(Q(category_id=1) || Q(category_id=2)) нижнее это примерно это
        # если нет _id=1 то выводится _id=2, а если есть то и 1 и 2
        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)

        action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) & \
                                Q(order_updated__lte=F('order__created') + action_2__time_delta)

        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)
