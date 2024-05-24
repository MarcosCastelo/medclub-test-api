from rest_framework import serializers
from items.models import Item
from utils.validators import validate_name, validate_price
from django.core.validators import MinValueValidator

class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validate_name])
    price = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
    
    class Meta:
        model = Item
        fields = ['id', 'name', 'price']
