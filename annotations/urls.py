from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnotationProjectViewSet, AnnotationImageViewSet

router = DefaultRouter()
router.register(r'projects', AnnotationProjectViewSet)
router.register(r'images', AnnotationImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

