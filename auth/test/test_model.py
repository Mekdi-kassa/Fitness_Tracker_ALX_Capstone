from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import CustomerRegister

User = get_user_model()

class CustomerRegisterModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'height': 175.5,
            'weight': 70.0,
            'fitness_goal': 'Weight Loss',
            'phone_number': '+1234567890'
        }

    def test_create_user(self):
        """Test creating a normal user"""
        user = CustomerRegister.objects.create_user(**self.user_data)
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.height, 175.5)
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = CustomerRegister.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
            height=180.0,
            weight=75.0
        )
        
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_email_unique(self):
        """Test that email must be unique"""
        CustomerRegister.objects.create_user(**self.user_data)
        
        with self.assertRaises(Exception):  # Should raise IntegrityError
            CustomerRegister.objects.create_user(
                email='test@example.com',  # Same email
                username='differentuser',
                password='testpass123',
                first_name='Jane',
                last_name='Doe',
                height=160.0,
                weight=60.0
            )

    def test_string_representation(self):
        """Test string representation of user"""
        user = CustomerRegister.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'test@example.com')

    def test_google_id_optional(self):
        """Test that google_id is optional"""
        user = CustomerRegister.objects.create_user(**self.user_data)
        self.assertIsNone(user.google_id)
        
        # Test with google_id
        user.google_id = 'google123'
        user.save()
        self.assertEqual(user.google_id, 'google123')