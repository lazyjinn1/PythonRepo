class ShoppingList(object):
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []
    
    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)
            print(f'{item} added to shopping list.')
        else:
            print(f'{item} is already in the shopping list.')
    
    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print(f'{item} removed from shopping list.')
        else:
            print(f'{item} is not currently in the shopping list.')
    def view_list(self):
        print(f'Current Shopping List: {self.shopping_list}')

    def merge_lists(self, obj):
        merged_list_name = 'Merged List - ' + str(self.list_name) + " + " + str(obj.list_name)

        merged_lists_obj = ShoppingList(merged_list_name)

        merged_lists_obj.shopping_list = self.shopping_list.copy()

        for item in merged_lists_obj.shopping_list:
            if item not in merged_lists_obj.shopping_list:
                merged_lists_obj.shopping_list.append(item)

        return merged_lists_obj



pet_store_list = ShoppingList('Pet Store Shopping List')
grocery_store_list = ShoppingList('Grocery Store List')
pet_store_list.add_item('dog food')
pet_store_list.add_item('frisbee')
pet_store_list.add_item('bowl')
pet_store_list.add_item('collars')
pet_store_list.add_item('flea collars')
pet_store_list.remove_item('flea collars')
pet_store_list.add_item('frisbee')
pet_store_list.view_list()

for item in ['dog food', 'frisbee', 'bowl', 'collars', 'flea collars']:
    pet_store_list.add_item(item.capitalize())

for item in ['fruits' ,'vegetables', 'bowl', 'ice cream']:
    grocery_store_list.add_item(item.capitalize())

new_list = pet_store_list.merge_lists(grocery_store_list)

new_list.view_list()