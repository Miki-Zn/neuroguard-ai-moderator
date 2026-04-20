from django.db import models
from django.conf import settings

class ContentItem(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),       
        ('processing', 'Processing'), 
        ('completed', 'Completed'),   
        ('failed', 'Failed'),         
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='content_items')
    text_content = models.TextField(blank=True, null=True, help_text="Text to be moderated")
    image_url = models.URLField(blank=True, null=True, help_text="URL of the image to be moderated")
    webhook_url = models.URLField(blank=True, null=True, help_text="Optional URL to receive async callback upon completion")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Content {self.id} by {self.user.username} - {self.status}"

class ModerationResult(models.Model):
    content_item = models.OneToOneField(ContentItem, on_delete=models.CASCADE, related_name='result')
    is_flagged = models.BooleanField(default=False, help_text="True if content violates policy")
    flagged_categories = models.JSONField(default=dict, blank=True, help_text="Specific violation categories")
    raw_response = models.JSONField(default=dict, blank=True, help_text="Raw JSON response from OpenAI")
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for Item {self.content_item.id} - Flagged: {self.is_flagged}"