from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract base model that provides created_at and updated_at fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
