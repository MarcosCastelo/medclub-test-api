from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User

class AuthenticationTests(TestCase):
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

    def test_register_user(self):
        response = self.client.post('/auth/register/', {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'phone_number': '123456789',
            'password': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_login_user(self):
        self.create_user('testuser', 'password', 'testuser@example.com')
        response = self.client.post('/auth/login/', {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_add_user_to_group(self):
        user = self.create_user('testuser', 'password', 'testuser@example.com')
        group = self.create_group('testgroup')
        user.groups.add(group)
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/auth/users/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('testgroup', [g['name'] for g in response.data['groups']])