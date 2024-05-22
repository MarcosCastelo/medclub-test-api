from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from items.models import Item

class ItemTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item1 = Item.objects.create(name='Test Item 1', price=10.0)
        self.item2 = Item.objects.create(name='Test Item 2', price=20.0)

    def test_item_creation(self):
        response = self.client.post('/items/', {'name': 'New Item', 'price': 15.0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 3)
        self.assertEqual(Item.objects.get(id=response.data['id']).name, 'New Item')

    def test_item_creation_invalid_name(self):
        response = self.client.post('/items/', {'name': 'No', 'price': 15.0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['error'])

    def test_item_creation_invalid_price(self):
        response = self.client.post('/items/', {'name': 'New Item', 'price': -10.0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data['error'])

    def test_item_list(self):
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_item_detail(self):
        response = self.client.get(f'/items/{self.item1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item 1')

    def test_item_update(self):
        response = self.client.put(f'/items/{self.item1.id}/', {'name': 'Updated Item', 'price': 30.0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(id=self.item1.id).name, 'Updated Item')

    def test_item_delete(self):
        response = self.client.delete(f'/items/{self.item1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 1)