from rest_framework import viewsets
from items.serializers import ItemSerializer
from items.models import Item
from utils.mixins import ExceptionHandlerMixin
from apps.authentication.permissions import IsGroupMemberOrReadOnly, IsAdminOrReadOnly

class ItemViewSet(ExceptionHandlerMixin, viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    required_groups = ['editors']
    permission_classes = [IsGroupMemberOrReadOnly]
