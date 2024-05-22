from rest_framework import viewsets, permissions
from items.serializers import ItemSerializer
from items.models import Item
from utils.mixins import ExceptionHandlerMixin

class ItemViewSet(ExceptionHandlerMixin, viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.AllowAny]
