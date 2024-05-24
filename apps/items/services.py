from items.models import Item

class  ItemService:
    @staticmethod
    def create_item(data):
        return Item.objects.create(**data)
    
    @staticmethod
    def update_item(item, data):
        for key, value in data.items():
            setattr(item, key, value)

        item.save()

    @staticmethod
    def delete_item(item):
        item.delete()

    @staticmethod
    def get_item(item_id):
        return Item.objects.get(id=item_id)
