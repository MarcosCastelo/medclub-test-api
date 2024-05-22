from orders.models import Order
from django.db import transaction

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(item_ids):
        order = Order.objects.create()
        order.items.set(item_ids)
        return order

    @staticmethod
    @transaction.atomic
    def update_order(order, item_ids):
        order.items.set(item_ids)
        order.save()
        return order

    @staticmethod
    def delete_order(order):
        order.delete()