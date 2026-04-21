from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import ContentItem
from .serializers import ContentItemSerializer
from .tasks import process_content_task

@extend_schema_view(
    list=extend_schema(description="Get a list of all moderation requests for the current user."),
    create=extend_schema(description="Submit a new text or image URL for asynchronous AI moderation."),
    retrieve=extend_schema(description="Get the detailed status and result of a specific moderation request.")
)

class ContentItemViewSet(viewsets.ModelViewSet):
    serializer_class = ContentItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContentItem.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        content_item = serializer.save(user=self.request.user)
        process_content_task.delay(content_item.id)

class AnalyticsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(description="Get overall metrics and a 7-day trend of moderation activity.")
    def get(self, request):
        user = request.user
        seven_days_ago = timezone.now() - timedelta(days=7)

        # 1. Overall metrics computed at the database level
        stats = ContentItem.objects.filter(user=user).aggregate(
            total_processed=Count('id'),
            flagged_count=Count('result', filter=Q(result__is_flagged=True)),
            failed_count=Count('id', filter=Q(status='failed'))
        )

        # 2. Time-series data for the last 7 days chart
        daily_stats = ContentItem.objects.filter(
            user=user,
            created_at__gte=seven_days_ago
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            daily_total=Count('id'),
            daily_flagged=Count('result', filter=Q(result__is_flagged=True))
        ).order_by('date')

        return Response({
            "overall": stats,
            "trend_last_7_days": daily_stats
        })