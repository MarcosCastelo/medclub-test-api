from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from items.models import Item
from django.contrib.auth.models import Group

class ItemTestCase(TestCase):
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

    def test_create_item_as_authorized_user(self):
        user = self.create_user('editor_user', 'password', 'editor@example.com')
        group = self.create_group('editors')
        user.groups.add(group)
        self.client.force_authenticate(user=user)
        response = self.client.post('/items/', {
            'name': 'Item 1',
            'price': 10.0,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)

    def test_create_item_as_unauthorized_user(self):
        user = self.create_user('normal_user', 'password', 'normal@example.com')
        self.client.force_authenticate(user=user)
        response = self.client.post('/items/', {
            'name': 'Item 1',
            'price': 10.0,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_items(self):
        normal_user = self.create_user('normal_user', 'password', 'normal@example.com')
        self.client.force_authenticate(user=normal_user)
        Item.objects.create(name='Item 1', price=10.0)
        Item.objects.create(name='Item 2', price=20.0)
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)