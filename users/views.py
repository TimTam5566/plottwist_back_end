'''
The Traffic Controller for applications.

This file handles HTTP requests - what happens when someone visits /users/ or /users/1/ or tries to log in.
'''

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserList(APIView):
    
    """
    Handles requests to /users/ (the list of all users)
    
    API ENDPOINT: /users/
    """

    def get(self, request):
        """
        HTTP GET /users/
        
        Returns a list of ALL users
        
        USED: If you wanted to show a list of all authors/contributors
        
        FLOW:
        1. Get all users from database
        2. Convert them to JSON using serializer
        3. Send back as response
        """
        users = CustomUser.objects.all() # Get all users from database
        serializer = CustomUserSerializer(users, many=True) # many=True because it's a LIST
        return Response(serializer.data) # Send back as JSON

    def post(self, request):
        """
        HTTP POST /users/
        
        Creates a NEW user (registration!)
        
        USED: When someone fills out the signup form
        
        FLOW:
        1. Take the data from the request (username, email, password)
        2. Validate it (is email valid? is password strong enough?)
        3. If valid, save to database and return success
        4. If invalid, return error messages
        """
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # This calls the create() method in serializer
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED # 201 = "Created successfully" all data sent is correct
            )
        # If data is invalid, return the errors
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST # 400 = "Bad request - something's wrong with the data sent"
        )
    
class CustomUserDetail(APIView):
    """
    Handles requests to /users/1/ (a SPECIFIC user by their ID)
    
    API ENDPOINT: /users/<id>/
    """
    def get_object(self, pk):
        """
        Finds a user by their primary key (ID)
        
        pk = "primary key" = the unique ID number
        
        If user doesn't exist, raises a 404 error (Not Found) Cant find what you're looking for!
        """
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404 # "User not found"

    def get(self, request, pk):
        """
        HTTP GET /users/1/
        
        Returns ONE specific user's info
        
        When viewing a user's profile
        """
        user = self.get_object(pk) # Find the user by their ID
        serializer = CustomUserSerializer(user) # Convert to JSON
        return Response(serializer.data) # Send back as JSON

class CustomAuthToken(ObtainAuthToken):
    """
    Handles LOGIN - when a user provides username/password to get their auth token
    
    API ENDPOINT: /api-token-auth/ (defined in main urls.py)
    
    A token is like a special key that proves who you are. Once you prove who you are
    by logging in, you get this key (token) that you can use to access protected parts 
    of the API. This allows the server to know it's really you making requests. It also allows you 
    to stay logged in without having to send your username and password every time.
    """
    def post(self, request, *args, **kwargs):
        """
        HTTP POST /api-token-auth/
        
        User sends username + password, gets back a token
        
        FLOW:
        1. User sends: {"username": "tim", "password": "secret123"}
        2. Django checks if credentials are correct
        3. If yes, create or get their token
        4. Send back: {"token": "abc123...", "user_id": 1, "email": "tim@email.com"}
        
        The frontend then stores this token and sends it with every future request
        """
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
            )
        serializer.is_valid(raise_exception=True) # Check credentials
        user = serializer.validated_data['user'] # Get the user object
        # Get existing token OR create a new one
        token, created = Token.objects.get_or_create(user=user)
        
        # Send back token + user info
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        })

