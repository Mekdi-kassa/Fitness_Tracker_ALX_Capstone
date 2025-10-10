from django.test import TestCase
from rest_framework.exceptions import ValidationError
from ..models import CustomerRegister
from ..serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    AvailabilityCheckSerializer,
    UserProfileSerializer
)

class UserRegistrationSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'height': 175.5,
            'weight': 70.0,
            'fitness_goal': 'Weight Loss',
            'phone_number': '+1234567890'
        }

    def test_valid_registration(self):
        """Test valid registration data"""
        serializer = UserRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        """Test password confirmation mismatch"""
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'differentpassword'
        
        serializer = UserRegistrationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_weak_password(self):
        """Test weak password validation"""
        weak_data = self.valid_data.copy()
        weak_data['password'] = '123'
        weak_data['password2'] = '123'
        
        serializer = UserRegistrationSerializer(data=weak_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_create_user(self):
        """Test user creation through serializer"""
        serializer = UserRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

class UserLoginSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomerRegister.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            height=175.5,
            weight=70.0
        )

    def test_valid_login_with_email(self):
        """Test login with email"""
        data = {'login': 'test@example.com', 'password': 'testpass123'}
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)

    def test_valid_login_with_username(self):
        """Test login with username"""
        data = {'login': 'testuser', 'password': 'testpass123'}
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)

    def test_invalid_credentials(self):
        """Test invalid login credentials"""
        data = {'login': 'test@example.com', 'password': 'wrongpassword'}
        serializer = UserLoginSerializer(data=data)
        
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_missing_credentials(self):
        """Test missing login credentials"""
        data = {'login': '', 'password': 'testpass123'}
        serializer = UserLoginSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('login', serializer.errors)

class AvailabilityCheckSerializerTest(TestCase):
    def test_valid_email_check(self):
        """Test email availability check"""
        data = {'email': 'test@example.com'}
        serializer = AvailabilityCheckSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_username_check(self):
        """Test username availability check"""
        data = {'username': 'testuser'}
        serializer = AvailabilityCheckSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_no_data_provided(self):
        """Test when no email or username provided"""
        data = {}
        serializer = AvailabilityCheckSerializer(data=data)
        self.assertFalse(serializer.is_valid())