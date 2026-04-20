import logging
import requests

logger = logging.getLogger(__name__)

def dispatch_webhook(webhook_url, payload):
    """
    Sends a POST request with the moderation results to the client's webhook URL.
    """
    if not webhook_url:
        return

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        logger.info(f"Webhook delivered successfully to {webhook_url}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to deliver webhook to {webhook_url}. Error: {str(e)}")