import jwt
import pytest
from django.urls import reverse
from umd_handle.api.models import Handle
from umd_handle.api.tokens import create_jwt_token
@pytest.fixture
def override_jwt_secret_setting(settings):
    """
    Overrides the JWT_SECRET setting with a value specific to the tests.
    """
    original_jwt_secret = settings.JWT_SECRET
    settings.JWT_SECRET = 'test_token_secret'

    yield
    settings.JWT_SECRET = original_jwt_secret

@pytest.fixture
def jwt_token(override_jwt_secret_setting) -> str:
    """
    Creates a JWT token using the JWT_SECRET for tests
    """
    return create_jwt_token('pytest test token')

@pytest.fixture
def handle1():
    """
    Creates a handle - 1903.1/1
    """
    return Handle.objects.create(prefix='1903.1', suffix = 1, url='http://example.com/')

@pytest.mark.django_db
def test_handles_prefix_suffix_requires_jwt_token(client):
    prefix = '1903.1'
    suffix = '1'
    response = client.get(reverse("handles_prefix_suffix", kwargs={'prefix': prefix, 'suffix': suffix}))
    assert response.status_code == 401

@pytest.mark.django_db
def test_handles_prefix_suffix_returns_known_handle(client, jwt_token, handle1):
    prefix = handle1.prefix
    suffix = handle1.suffix
    headers = { 'Authorization': f"Bearer {jwt_token}" }
    response = client.get(reverse("handles_prefix_suffix", kwargs={'prefix': prefix, 'suffix': suffix}),
                           headers=headers)
    assert response.status_code == 200

@pytest.mark.django_db
def test_handles_prefix_suffix_returns_404_for_unknown_handle(client, jwt_token):
    prefix = 'UNKNOWN_PREFIX'
    suffix = 1
    headers = { 'Authorization': f"Bearer {jwt_token}" }
    response = client.get(reverse("handles_prefix_suffix", kwargs={'prefix': prefix, 'suffix': suffix}),
                           headers=headers)
    assert response.status_code == 404


