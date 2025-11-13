from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel

def validate_prefix(value):
    if value not in Handle.ALLOWED_PREFIXES:
        raise ValidationError(f"'{value}' is not an allowed prefix.")

class Handle(TimeStampedModel):

    ALLOWED_PREFIXES = [
        '1903.1',
    ]

    prefix = models.CharField(
        choices=[(prefix, prefix) for prefix in ALLOWED_PREFIXES],
        validators=[validate_prefix]
    )
    suffix = models.IntegerField()
    url = models.CharField()
    repo = models.CharField()
    repo_id = models.CharField()
    description = models.CharField(blank=True)
    notes = models.TextField(blank=True)

class JWTToken(TimeStampedModel):
    token = models.CharField()
    description = models.CharField()
