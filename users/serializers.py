from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomerRegister
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomerRegister
        fields = ('id', 'email', 'username', 'password', 'password2', 
                 'first_name', 'last_name', 'height', 'weight', 
                 'fitness_goal', 'phone_number')
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = CustomerRegister.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
class UserLoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        if not login:
            raise serializers.ValidationError('Email / Username is required')
        if not password:
            raise serializers.ValidationError("Password is required.")

        user = authenticate(username = login, password = password)

        if not user:
            try:
                user_obj = CustomerRegister.objects.get(username = login)
                user = authenticate(username = user_obj.email , password = password)
            except:
                user = None
        
        if not user:
            raise serializers.ValidationError("Invalid email/password !!")
        
        attrs['user'] =user
        return attrs
class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = CustomerRegister
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 
                 'height', 'weight', 'fitness_goal', 'phone_number', 
                 'picture_url')
        read_only_fields = ('email',)

class GoogleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(required = False)
    id_token = serializers.CharField(required = False)
    code = serializers.CharField(required=False)

class AvailabilityCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(required = False)
    username = serializers.CharField(required = False)

    def validate(self,attrs):
        if not attrs.get('email') and not attrs.get('username'):
            raise serializers.ValidationError("Either email or username must be provided")
        return attrs

# Provide the serializer under the name tests expect
UserProfileSerializer = UserProfile
