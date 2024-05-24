from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.authentication.models import User
from apps.items.models import Item
from orders.models import Order, OrderItem
from django.contrib.auth.models import Group

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_user(self, username, password, email, is_admin=False):
        user = User.objects.create_user(username=username, password=password, email=email)
        if is_admin:
            user.is_superuser = True
            user.is_staff = True
            user.save()
        return user

    def create_group(self, name):
        group, created = Group.objects.get_or_create(name=name)
        return group

    def create_item(self, name, price):
        return Item.objects.create(name=name, price=price, description='A sample item.')

    def test_create_order(self):
        user = self.create_user('normal_user', 'password', 'normal@example.com')
        item = self.create_item('Item 1', 10.0)
        self.client.force_authenticate(user=user)
        response = self.client.post('/orders/', {
            'order_items': [
                {'item_id': item.id, 'quantity': 2}
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_list_orders_as_normal_user(self):
        user = self.create_user('normal_user', 'password', 'normal@example.com')
        item = self.create_item('Item 1', 10.0)
        order = Order.objects.create(user=user)
        OrderItem.objects.create(order=order, item=item, quantity=2, price=20.0)
        self.client.force_authenticate(user=user)
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_orders_as_authorized_user(self):
        user = self.create_user('manager_user', 'password', 'manager@example.com')
        group = self.create_group('order_managers')
        user.groups.add(group)
        normal_user = self.create_user('normal_user', 'password', 'normal@example.com')
        item = self.create_item('Item 1', 10.0)
        order = Order.objects.create(user=normal_user)
        OrderItem.objects.create(order=order, item=item, quantity=2, price=20.0)
        self.client.force_authenticate(user=user)
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_order_as_admin(self):
        admin_user = self.create_user('admin_user', 'password', 'admin@example.com', is_admin=True)
        normal_user = self.create_user('normal_user', 'password', 'normal@example.com')
        item = self.create_item('Item 1', 10.0)
        order = Order.objects.create(user=normal_user)
        OrderItem.objects.create(order=order, item=item, quantity=2, price=20.0)
        self.client.force_authenticate(user=admin_user)
        response = self.client.delete(f'/orders/{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)