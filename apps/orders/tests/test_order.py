from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from orders.models import Order, OrderItem
from items.models import Item

class OrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item1 = Item.objects.create(name='Test Item 1', price=10.0)
        self.item2 = Item.objects.create(name='Test Item 2', price=20.0)
        self.order = Order.objects.create()
        self.order_item1 = OrderItem.objects.create(order=self.order, item=self.item1, quantity=2)
        self.order_item2 = OrderItem.objects.create(order=self.order, item=self.item2, quantity=1)

    def test_order_creation(self):
        response = self.client.post('/orders/', {'order_items': [{'item': str(self.item1.id), 'quantity': 2}, {'item': str(self.item2.id), 'quantity': 1}]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=response.data['id']).order_items.count(), 2)
        self.assertEqual(Order.objects.get(id=response.data['id']).total_price, 40.0)

    def test_order_creation_no_items(self):
        response = self.client.post('/orders/', {'order_items': []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('order_items', response.data.get('error'))

    def test_order_list(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_detail(self):
        response = self.client.get(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.order.id))

    def test_order_update(self):
        response = self.client.put(f'/orders/{self.order.id}/', {'order_items': [{'item': str(self.item1.id), 'quantity': 3}]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(id=self.order.id).order_items.count(), 1)
        self.assertEqual(Order.objects.get(id=self.order.id).total_price, 30.0)

    def test_order_update_no_items(self):
        response = self.client.put(f'/orders/{self.order.id}/', {'order_items': []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('order_items', response.data.get('error'))

    def test_order_delete(self):
        response = self.client.delete(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)