from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnotationProjectViewSet, AnnotationImageViewSet
from .auth import RegisterView, LoginView, UserProfileView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'projects', AnnotationProjectViewSet)
router.register(r'images', AnnotationImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
