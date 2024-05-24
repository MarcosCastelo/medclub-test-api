from rest_framework import viewsets, permissions, filters
from items.serializers import ItemSerializer
from items.models import Item
from utils.mixins import ExceptionHandlerMixin
from authentication.permissions import IsGroupMemberOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class ItemViewSet(ExceptionHandlerMixin, viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    required_groups = ['editors']
    permission_classes = [permissions.IsAuthenticated, IsGroupMemberOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'price']
    ordering_fields = ['name', 'price']
