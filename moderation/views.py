from rest_framework import viewsets, permissions
from .models import ContentItem
from .serializers import ContentItemSerializer

class ContentItemViewSet(viewsets.ModelViewSet):
    serializer_class = ContentItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Security: Users can only access their own moderation history
        return ContentItem.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Auto-assign the user making the request
        content_item = serializer.save(user=self.request.user)
        
        # NOTE: In Day 4, we will trigger the Celery task here:
        # process_content_task.delay(content_item.id)