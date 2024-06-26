# Generated by Django 5.0.6 on 2024-05-23 19:28

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinValueValidator(3, 'The name must have at least 3 characters.')])),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0, 'The price must be positive.')])),
            ],
        ),
    ]
