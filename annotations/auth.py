from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    """
    API endpoint for user registration.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        description="Register a new user",
        request=RegisterSerializer,
        responses={
            201: UserSerializer,
            400: serializers.Serializer
        },
        examples=[
            OpenApiExample(
                'Valid Registration',
                value={
                    'username': 'newuser',
                    'email': 'user@example.com',
                    'password': 'strongpassword123',
                    'password2': 'strongpassword123',
                    'first_name': 'John',
                    'last_name': 'Doe'
                }
            )
        ]
    )
    def post(self, request):
        """
        Create a new user account.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    API endpoint for user login.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        description="Login with email and password",
        request=LoginSerializer,
        responses={
            200: LoginSerializer,
        },
        examples=[
            OpenApiExample(
                'Successful Login',
                value={
                    'email': 'user@example.com',
                    'password': 'yourpassword'
                }
            )
        ]
    )
    def post(self, request):
        """
        Authenticate user and return JWT tokens.
        """
        email = request.data.get('email')
        password = request.data.get('password')

        # Try to authenticate using email
        user = User.objects.filter(email=email).first()
        
        if user:
            # Authenticate with username (which is the email)
            authenticated_user = authenticate(
                username=user.username, 
                password=password
            )

            if authenticated_user:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(authenticated_user)
                return Response({
                    'user': UserSerializer(authenticated_user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })

        return Response({
            'detail': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    """
    API endpoint for user profile management.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Retrieve current user's profile",
        responses={200: UserSerializer}
    )
    def get(self, request):
        """
        Get the current authenticated user's profile.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        description="Update current user's profile",
        request=UserSerializer,
        responses={200: UserSerializer},
        examples=[
            OpenApiExample(
                'Partial Update',
                value={
                    'first_name': 'Updated Name',
                    'email': 'newemail@example.com'
                }
            )
        ]
    )
    def patch(self, request):
        """
        Partially update the current user's profile.
        """
        serializer = UserSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)