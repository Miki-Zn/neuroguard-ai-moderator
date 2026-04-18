import time
from celery import shared_task
from .models import ContentItem

@shared_task
def process_content_task(content_item_id):
    try:
        item = ContentItem.objects.get(id=content_item_id)
        
        item.status = 'processing'
        item.save()

        # TODO: implement OpenAI API call here
        # using sleep temporarily to test celery worker queue
        time.sleep(3)

        item.status = 'completed'
        item.save()
        
        return f"Task completed for item ID {content_item_id}"
        
    except ContentItem.DoesNotExist:
        return f"Error: Item {content_item_id} not found."