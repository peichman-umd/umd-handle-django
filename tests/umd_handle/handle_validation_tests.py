import pytest
from django.core.exceptions import ValidationError
from umd_handle.api.models import Handle

@pytest.fixture
def valid_handle():
    valid_handle = Handle(
        prefix='1903.1',
        suffix=1,
        url='http://example.com/valid-handle',
        repo='avalon',
        repo_id='avalon:valid-handle'
    )
    valid_handle.full_clean()
    valid_handle.save()
    return valid_handle

@pytest.mark.django_db
def test_prefix_must_be_known_prefix(valid_handle):
    handle = valid_handle
    handle.prefix = 'INVALID_PREFIX'

    with pytest.raises(ValidationError):
        handle.full_clean()

@pytest.mark.django_db
def test_prefix_must_be_known_repo(valid_handle):
    handle = valid_handle
    handle.repo = 'INVALID_REPO'

    with pytest.raises(ValidationError):
        handle.full_clean()

@pytest.mark.django_db
def test_combined_prefix_and_suffix_must_be_unique(valid_handle):
    duplicate_handle = Handle(
        prefix=valid_handle.prefix,
        suffix=valid_handle.suffix,
        url='http://example.com/duplicate-handle',
        repo='fcrepo',
        repo_id='fcrepo:duplicate-handle'
    )

    with pytest.raises(ValidationError):
        duplicate_handle.full_clean()
