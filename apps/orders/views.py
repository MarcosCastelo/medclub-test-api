from utils.mixins import ExceptionHandlerMixin
from rest_framework import viewsets, permissions, status
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.services import OrderService
from rest_framework.response import Response

class OrderViewSet(ExceptionHandlerMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        order_items_data = serializer.validated_data.pop('order_items')
        order = OrderService.create_order(order_items_data)
        serializer.instance = order

    def perform_update(self, serializer):
        order_items_data =serializer.validated_data.pop('order_items')
        order = OrderService.update_order(self.get_object(), order_items_data)
        serializer.instance = order
