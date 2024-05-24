from utils.mixins import ExceptionHandlerMixin
from rest_framework import viewsets, permissions
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.services import OrderService
from apps.authentication.permissions import IsAdminOrReadOnly, IsGroupMemberOrOwnerOrReadOnly

class OrderViewSet(ExceptionHandlerMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    required_groups = ['manager']
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated],
        'list': [permissions.IsAuthenticated],
        'retrieve': [IsGroupMemberOrOwnerOrReadOnly],
        'update': [IsGroupMemberOrOwnerOrReadOnly],
        'partial_update': [IsGroupMemberOrOwnerOrReadOnly],
        'destroy': [IsAdminOrReadOnly]
    }
    
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
    
    def get_queryset(self):
        user_group_names = [group.name for group in self.request.user.groups.all()]
        if any(group in user_group_names for group in self.required_groups):
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        order_items_data = serializer.validated_data.pop('order_items')
        order = OrderService.create_order(user=self.request.user, order_items_data=order_items_data)
        serializer.instance = order

    def perform_update(self, serializer):
        order_items_data =serializer.validated_data.pop('order_items')
        order = OrderService.update_order(order=self.get_object(), order_items_data=order_items_data)
        serializer.instance = order
