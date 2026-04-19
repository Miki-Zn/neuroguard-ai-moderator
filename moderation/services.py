import json
import logging
from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_content_text(text_content):
    prompt = """
    Analyze the following text for moderation purposes.
    Determine if it contains spam, hate speech, or harassment.
    Return ONLY a JSON object with the exact following structure:
    {
        "is_flagged": boolean,
        "flagged_categories": {
            "spam": boolean,
            "hate_speech": boolean,
            "harassment": boolean
        }
    }
    Text to analyze:
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a strict content moderation API. You output valid JSON only."},
                {"role": "user", "content": f"{prompt}\n{text_content}"}
            ],
            response_format={ "type": "json_object" }
        )
        
        result_str = response.choices[0].message.content
        result = json.loads(result_str)
        return result, response.model_dump()
        
    except Exception as e:
        logger.error(f"OpenAI API Integration Error: {str(e)}")
        return None, None