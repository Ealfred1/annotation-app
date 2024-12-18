from django.db import models
from django.contrib.auth.models import User
import uuid

class AnnotationProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class AnnotationImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(AnnotationProject, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.filename

class Annotation(models.Model):
    ANNOTATION_TYPES = [
        ('BBOX', 'Bounding Box'),
        ('POLYGON', 'Polygon'),
        ('POINT', 'Point'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(AnnotationImage, related_name='annotations', on_delete=models.CASCADE)
    annotation_type = models.CharField(max_length=10, choices=ANNOTATION_TYPES)
    data = models.JSONField()  # Store annotation coordinates
    label = models.CharField(max_length=100)
    annotator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.label} - {self.annotation_type}"