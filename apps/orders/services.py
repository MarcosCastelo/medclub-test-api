from orders.models import Order, OrderItem
from django.db import transaction

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(order_items_data):
        order = Order.objects.create()
        total_price = 0
        for order_item_data in order_items_data:
            item = order_item_data['item']
            quantity = order_item_data['quantity']
            order_item = OrderItem.objects.create(order=order, item=item, quantity=quantity)
            total_price += order_item.price
        order.total_price = total_price
        order.save()
        return order

    @staticmethod
    @transaction.atomic
    def update_order(order, order_items_data):
        order.order_items.all().delete()
        total_price = 0
        for order_item_data in order_items_data:
            item = order_item_data['item']
            quantity = order_item_data['quantity']
            order_item = OrderItem.objects.create(order=order, item=item, quantity=quantity)
            total_price += order_item.price
        order.total_price = total_price
        order.save()
        return order