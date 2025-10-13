from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import CustomerRegister

class AuthenticationAPITest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.check_availability_url = reverse('check-availability')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('get-profile')
        
        self.valid_user_data = {
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
        
        # Create a test user
        self.user = CustomerRegister.objects.create_user(
            email='existing@example.com',
            username='existinguser',
            password='existingpass123',
            first_name='Existing',
            last_name='User',
            height=180.0,
            weight=75.0
        )

    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully')
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)
        
        # Check if user was created in database
        self.assertTrue(CustomerRegister.objects.filter(email='test@example.com').exists())

    def test_user_registration_password_mismatch(self):
        """Test registration with password mismatch"""
        invalid_data = self.valid_user_data.copy()
        invalid_data['password2'] = 'differentpassword'
        
        response = self.client.post(self.register_url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Registration failed')
        self.assertIn('password', response.data['errors'])

    def test_user_login_success_with_email(self):
        """Test successful login with email"""
        login_data = {'login': 'existing@example.com', 'password': 'existingpass123'}
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login successful')
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)

    def test_user_login_success_with_username(self):
        """Test successful login with username"""
        login_data = {'login': 'existinguser', 'password': 'existingpass123'}
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login successful')

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {'login': 'existing@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Login failed')

    def test_check_email_availability(self):
        """Test email availability check"""
        # Check available email
        response = self.client.post(self.check_availability_url, {'email': 'new@example.com'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['email_available'])
        
        # Check taken email
        response = self.client.post(self.check_availability_url, {'email': 'existing@example.com'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['email_available'])

    def test_check_username_availability(self):
        """Test username availability check"""
        # Check available username
        response = self.client.post(self.check_availability_url, {'username': 'newuser'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['username_available'])
        
        # Check taken username
        response = self.client.post(self.check_availability_url, {'username': 'existinguser'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['username_available'])

    def test_get_user_profile_authenticated(self):
        """Test getting user profile when authenticated"""
        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        # Set authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], 'existing@example.com')

    def test_get_user_profile_unauthenticated(self):
        """Test getting user profile without authentication"""
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout(self):
        """Test user logout"""
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        logout_data = {'refresh': str(refresh)}
        response = self.client.post(self.logout_url, logout_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful')