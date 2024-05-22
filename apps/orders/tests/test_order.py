from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from orders.models import Order
from apps.items.models import Item

class OrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item1 = Item.objects.create(name='Test Item 1', price=10.0)
        self.item2 = Item.objects.create(name='Test Item 2', price=20.0)
        self.order = Order.objects.create(user=self.user)
        self.order.items.set([self.item1, self.item2])

    def test_order_creation(self):
        response = self.client.post('/orders/', {'items': [str(self.item1.id), str(self.item2.id)]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=response.data['id']).items.count(), 2)

    def test_order_creation_no_items(self):
        response = self.client.post('/orders/', {'items': []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_order_list(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_detail(self):
        response = self.client.get(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.order.id))

    def test_order_update(self):
        response = self.client.put(f'/orders/{self.order.id}/', {'items': [str(self.item1.id)]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(id=self.order.id).items.count(), 1)

    def test_order_update_no_items(self):
        response = self.client.put(f'/orders/{self.order.id}/', {'items': []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_order_delete(self):
        response = self.client.delete(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)