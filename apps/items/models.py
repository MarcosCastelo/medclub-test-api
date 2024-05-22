import uuid
from django.db import models
from django.core.validators import MinValueValidator

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, validators=[
        MinValueValidator(3, "The name must have at least 3 characters.")
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0, "The price must be positive.")
    ])

    def __str__(self):
        return self.name

