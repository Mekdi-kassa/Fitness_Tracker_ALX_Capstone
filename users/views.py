from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
import requests
from .models import CustomerRegister
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfile,
    GoogleAuthSerializer, AvailabilityCheckSerializer, UserProfile as UserProfileSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def check_availability(request):
    serializer = AvailabilityCheckSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')

        response_data = {}
        if email:
            email_exist = CustomerRegister.objects.filter(email__iexact=email).exists()
            response_data['email_available'] = not email_exist
            response_data['email'] = email
        if username:
            username_exists = CustomerRegister.objects.filter(username__iexact=username).exists()
            response_data['username_available'] = not username_exists
            response_data['username'] = username
        return Response(response_data)
    
    return Response({
        'message': 'validation failed',
        'error': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)

        return Response({
            'message': 'User registered successfully',
            'user': UserProfileSerializer(user).data,
            'tokens':{
                'refresh' : str(refresh_token),
                'access' :str(refresh_token.access_token)
            }
        },
        status = status.HTTP_201_CREATED
        )
    return Response({
        'message': 'Registration failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'user': UserProfileSerializer(user).data,  # Return user profile
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    return Response({
        'message': 'Login failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response({
        'user': serializer.data
    })
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only logged-in users can logout
def logout_user(request):
    """
    User logout API
    Expected JSON: {"refresh": "refresh_token"}
    """
    try:
        refresh_token = request.data.get("refresh")  # Get refresh token from request
        if refresh_token:
            token = RefreshToken(refresh_token)  # Create RefreshToken object
            try:
                token.blacklist()  # Add token to blacklist (can't be used again)
            except Exception:
                # If blacklist app isn't configured, ignore and proceed
                pass
        
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)  # HTTP 200 OK
        
    except Exception as e:  # If logout fails
        return Response({
            'message': 'Logout failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """
    Google OAuth login/registration
    Expected JSON: {"access_token": "google_access_token"} OR {"id_token": "google_id_token"}
    """
    serializer = GoogleAuthSerializer(data=request.data)  # Validate Google auth data
    
    if not serializer.is_valid():  # If token validation fails
        return Response({
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    access_token = serializer.validated_data.get('access_token')  # Get access token
    id_token = serializer.validated_data.get('id_token')  # Get ID token
    
    try:
        # Verify Google token and get user info
        if access_token:
            # Use access token to get user info from Google
            user_info = requests.get(
                'https://www.googleapis.com/oauth2/v1/userinfo',
                params={'access_token': access_token}
            ).json()  # Convert response to JSON
        elif id_token:
            # Verify ID token with Google
            user_info = requests.get(
                'https://www.googleapis.com/oauth2/v3/tokeninfo',
                params={'id_token': id_token}
            ).json()
        else:
            return Response({
                'message': 'Either access_token or id_token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if 'error' in user_info:  # If Google returned an error
            return Response({
                'message': 'Invalid Google token',
                'error': user_info['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract user information from Google response
        google_id = user_info['sub']  # Unique Google user ID
        email = user_info['email']  # User's email
        first_name = user_info.get('given_name', '')  # First name (default to empty)
        last_name = user_info.get('family_name', '')  # Last name (default to empty)
        picture_url = user_info.get('picture', '')  # Profile picture URL
        
        # Check if user exists with this Google ID
        try:
            user = CustomerRegister.objects.get(google_id=google_id)  # Find by Google ID
        except CustomerRegister.DoesNotExist:
            # If no Google ID match, check if user exists with this email
            try:
                user = CustomerRegister.objects.get(email=email)  # Find by email
                user.google_id = google_id  # Link Google account to existing user
                user.picture_url = picture_url  # Update profile picture
                user.save()
            except CustomerRegister.DoesNotExist:
                # Create new user since no existing account found
                username = email.split('@')[0]  # Use email prefix as base username
                # Ensure username is unique
                base_username = username
                counter = 1
                while CustomerRegister.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"  # Append number if exists
                    counter += 1
                
                # Create new user with Google data
                user = CustomerRegister.objects.create(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    google_id=google_id,
                    picture_url=picture_url,
                    height=0.0,  # Default values (user can update later)
                    weight=0.0,
                    is_active=True  # Activate the user
                )
                user.set_unusable_password()  # Google users don't need password
                user.save()
        
        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Google login successful',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
        
    except Exception as e:  # Catch any unexpected errors
        return Response({
            'message': 'Google login failed',
            'error': str(e)  # Return error message
        }, status=status.HTTP_400_BAD_REQUEST)