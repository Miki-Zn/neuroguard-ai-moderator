from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentItemViewSet

router = DefaultRouter()
router.register(r'items', ContentItemViewSet, basename='content-item')

urlpatterns = [
    path('', include(router.urls)),
]