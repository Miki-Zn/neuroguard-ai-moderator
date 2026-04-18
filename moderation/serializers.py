from rest_framework import serializers
from .models import ContentItem, ModerationResult

class ModerationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationResult
        fields = ['is_flagged', 'flagged_categories', 'analyzed_at']

class ContentItemSerializer(serializers.ModelSerializer):
    result = ModerationResultSerializer(read_only=True)

    class Meta:
        model = ContentItem
        fields = ['id', 'text_content', 'image_url', 'status', 'created_at', 'result']
        read_only_fields = ['status', 'created_at']

    def validate(self, data):
        """
        Check that either text or image_url is provided.
        """
        if not data.get('text_content') and not data.get('image_url'):
            raise serializers.ValidationError("You must provide either 'text_content' or 'image_url'.")
        return data