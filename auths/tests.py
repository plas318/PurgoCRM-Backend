from django.test import TestCase
from .models import User

class CustomUserTests(TestCase):
    def setUp(self):
        self.User = User
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass',
            name='test1',
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('testpass'))

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass',
            name='test2',
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)