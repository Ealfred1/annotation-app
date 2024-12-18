from rest_framework import serializers
from .models import AnnotationProject, AnnotationImage, Annotation

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