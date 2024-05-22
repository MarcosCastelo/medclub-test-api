from rest_framework import serializers
from orders.models import Order
from items.models import Item

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), many=True)
    
    class Meta:
        model = Order
        fields = ['id', 'items', 'created_at']
        read_only_fields = ['created_at']
        
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("A order must to have at least one item.")
        return value