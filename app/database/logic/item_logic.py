from database.models.item import Item 

def get_item(id):
    return Item.objects.filter(id=id).first()

def get_items_for_restaurant(store_name):
    return Item.objects.filter(store=store_name)

def create_item(**kwargs):
    new_item = Item(**kwargs)
    new_item.save()

def delete_item(id):
    item = get_item(id)
    item.delete()

