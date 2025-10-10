from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class BasicModelTest(TestCase):
    def test_create_user(self):
        """Test that we can create a basic user"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            height=175.0,
            weight=70.0
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        print("✅ Basic user creation test passed!")
        
    def test_string_representation(self):
        """Test the string representation of user"""
        user = User.objects.create_user(
            email='john@example.com',
            username='john',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            height=180.0,
            weight=75.0
        )
        
        self.assertEqual(str(user), 'john@example.com')
        print("✅ String representation test passed!")