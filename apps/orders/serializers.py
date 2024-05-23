from rest_framework import serializers
from orders.models import Order, OrderItem
from items.models import Item

class ItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    item_detail = ItemDetailSerializer(source='item', read_only=True)
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    
    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'item_detail', 'quantity', 'price']
        read_only_fields = ['price']
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("The quantity must be positive")
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'request' in self.context:
            view = self.context['view']
            if view.action == 'list':
                representation.pop('item_detail', None)
            else:
                representation.pop('item', None)
        return representation

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_items', 'total_price', 'created_at']
        read_only_fields = ['created_at', 'total_price']
        
    def validate_order_items(self, value):
        if not value:
            raise serializers.ValidationError('Order must have at least a item.')
        return value