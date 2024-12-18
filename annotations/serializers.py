from rest_framework import serializers
from .models import AnnotationProject, AnnotationImage, Annotation
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ['id', 'annotation_type', 'data', 'label', 'created_at']

class AnnotationImageSerializer(serializers.ModelSerializer):
    annotations = AnnotationSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnnotationImage
        fields = ['id', 'image', 'filename', 'uploaded_at', 'annotations']

class AnnotationProjectSerializer(serializers.ModelSerializer):
    images = AnnotationImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnnotationProject
        fields = ['id', 'name', 'description', 'created_at', 'images']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password', 
            'password2', 
            'first_name', 
            'last_name'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        # Remove password2 before creating user
        validated_data.pop('password2')
        
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)