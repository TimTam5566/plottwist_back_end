'''
This is the TRANSLATOR FILE for the users app. 

This file converts data between what React sends (JSON) 
and what Django uses (Python objects), and ensures passwords are properly encrypted.

Why is this important?
serialisers.py defines how CustomUser model instances are converted to and from JSON. 
'''

from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """
    WHAT THIS IS:
    A serializer TRANSLATES data between two formats:
    1. Python objects (what Django uses internally)
    2. JSON (what the React frontend sends/receives)
    
    This is like a translator between two people speaking different languages.
    
    WHEN DATA COMES IN (from React):
    JSON {"username": "tim", "password": "secret123"} 
        → Serializer validates it
        → Creates a Python User object
        → Saves to database
    
    WHEN DATA GOES OUT (to React):
    Python User object 
        → Serializer converts it
        → JSON {"id": 1, "username": "tim", "email": "tim@email.com"}
    """
    class Meta:
        model = CustomUser # "This serializer is for the CustomUser model"
        fields = '__all__' # "Include all fields from the model"
        extra_kwargs = {'password': {'write_only': True}}
        # ^^^ SECURITY: Password can be SENT IN but never SENT OUT
        # So when you GET a user, their password isn't exposed

    def create(self, validated_data):
        """
        When creating a new user, create_user() is used instead of just create()
        
        create_user() automatically HASHES the password (encrypts it)
        If we used regular create(), the password would be stored as plain text which is a security risk.
        
        Example:
        - User types: "mypassword123"
        - create_user() stores: "pbkdf2_sha256$390000$abc123..."  (encrypted)
        """
        return CustomUser.objects.create_user(**validated_data)