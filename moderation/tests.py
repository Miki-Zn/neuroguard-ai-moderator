import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from moderation.models import ContentItem

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser', 
        email='test@example.com', 
        password='password123'
    )

@pytest.mark.django_db
@patch('moderation.views.process_content_task.delay')
def test_create_content_item(mock_task, api_client, test_user):
    """
    Test that an authenticated user can submit text for moderation,
    and the background Celery task is triggered.
    """
    api_client.force_authenticate(user=test_user)
    payload = {"text_content": "This is a test message"}
    
    response = api_client.post('/api/v1/moderation/items/', payload)
    
    assert response.status_code == 201
    assert ContentItem.objects.count() == 1
    
    created_item = ContentItem.objects.first()
    assert created_item.status == 'pending'
    
    # Ensure Celery task was called with the correct ID
    mock_task.assert_called_once_with(created_item.id)

@pytest.mark.django_db
def test_unauthenticated_access(api_client):
    """
    Test that unauthenticated users cannot access the API.
    """
    response = api_client.get('/api/v1/moderation/items/')
    assert response.status_code == 401