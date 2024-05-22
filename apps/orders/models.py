import uuid
from django.db import models
from items.models import Item

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True)