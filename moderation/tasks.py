from celery import shared_task
import logging
from .models import ContentItem, ModerationResult
from .services import analyze_content_text

logger = logging.getLogger(__name__)

@shared_task
def process_content_task(content_item_id):
    try:
        item = ContentItem.objects.get(id=content_item_id)
        
        if item.text_content:
            analysis_result, raw_response = analyze_content_text(item.text_content)
            
            if analysis_result:
                ModerationResult.objects.create(
                    content_item=item,
                    is_flagged=analysis_result.get('is_flagged', False),
                    flagged_categories=analysis_result.get('flagged_categories', {}),
                    raw_response=raw_response or {}
                )
                item.status = 'completed'
            else:
                item.status = 'failed'
        else:
            item.status = 'failed'
            
        item.save()
        return f"Task completed for item ID {content_item_id}"
        
    except ContentItem.DoesNotExist:
        return f"Error: Item {content_item_id} not found."

@shared_task
def daily_maintenance_script():
    logger.info("Executing automatic daily cron job script...")
    
    # Example maintenance: count and log failed items, retry logic, or db cleanup
    failed_items = ContentItem.objects.filter(status='failed')
    count = failed_items.count()
    
    logger.info(f"Daily script executed successfully. Processed {count} failed items.")
    return count