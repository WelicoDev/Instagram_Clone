import uuid

from django.db import models

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(unique=True , primary_key=True, default=uuid.uuid4() , editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True