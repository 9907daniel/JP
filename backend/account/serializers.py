from django.contrib.auth.models import User
from rest_framework import serializers

class SignUpSerializer(serializers.ModelSerializer):
    # Model Meta is basically the inner class of your model class. Model Meta is basically used to change the behavior of your model fields
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},              
        }
        
class UserSerializer(serializers.ModelSerializer):
    resume = serializers.CharField(source="userprofile.resume")
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'resume') 