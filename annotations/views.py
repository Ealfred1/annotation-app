# backend/annotations/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AnnotationProject, AnnotationImage, Annotation
from .serializers import (
    AnnotationProjectSerializer, 
    AnnotationImageSerializer, 
    AnnotationSerializer
)

class AnnotationProjectViewSet(viewsets.ModelViewSet):
    queryset = AnnotationProject.objects.all()
    serializer_class = AnnotationProjectSerializer

    @action(detail=True, methods=['POST'])
    def upload_image(self, request, pk=None):
        project = self.get_object()
        image_file = request.FILES.get('image')
        
        if not image_file:
            return Response({'error': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create AnnotationImage instance
        annotation_image = AnnotationImage.objects.create(
            project=project,
            image=image_file,
            filename=image_file.name
        )
        
        serializer = AnnotationImageSerializer(annotation_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AnnotationImageViewSet(viewsets.ModelViewSet):
    queryset = AnnotationImage.objects.all()
    serializer_class = AnnotationImageSerializer

    @action(detail=True, methods=['POST'])
    def add_annotation(self, request, pk=None):
        image = self.get_object()
        
        annotation_data = {
            'image': image,
            'annotation_type': request.data.get('annotation_type', 'BBOX'),
            'data': request.data.get('data', {}),
            'label': request.data.get('label', 'Unlabeled'),
            'annotator': request.user if request.user.is_authenticated else None
        }
        
        annotation = Annotation.objects.create(**annotation_data)
        serializer = AnnotationSerializer(annotation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

