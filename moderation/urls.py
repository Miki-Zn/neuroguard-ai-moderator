from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentItemViewSet, AnalyticsView

router = DefaultRouter()
router.register(r'items', ContentItemViewSet, basename='content-item')

urlpatterns = [
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('', include(router.urls)),
]