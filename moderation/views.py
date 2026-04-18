from rest_framework import viewsets, permissions
from .models import ContentItem
from .serializers import ContentItemSerializer

class ContentItemViewSet(viewsets.ModelViewSet):
    serializer_class = ContentItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContentItem.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        
        content_item = serializer.save(user=self.request.user)
        
        
        from .tasks import process_content_task
        process_content_task.delay(content_item.id)