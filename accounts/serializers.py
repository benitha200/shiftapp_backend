# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'role','first_name', 'last_name')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('email', 'username', 'role','first_name', 'last_name')