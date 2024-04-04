import pickle

def display_recipe(recipe):
    print('Recipe Name: ', recipe['Name'])
    print('Cooking Time: ', recipe['Cooking Time'], ' minutes')
    print('Ingredients: ', recipe['Ingredients'])
    print('Difficulty: ', recipe['Difficulty'])


def search_ingredient(data):
    print("Ingredients: ")
    for index, ingredient in enumerate(data['ingredients_list']):
        all_ingredients = index, ingredient
        print(all_ingredients)
    try:
        ingredient_index = int(input('Choose an ingredient (by number): '))
        if 0 <= ingredient_index < len(data['ingredients_list']):
            ingredient_name = data['ingredients_list'][ingredient_index]
            print('You have chosen: ', ingredient_name)
        else:
            print('Invalid ingredient number. ')
            return
    except ValueError:
        print('The chosen number is of an incorrect type. It needs to be of type int')
    else:
        for recipe in data['recipes_list']:
            if ingredient_name in recipe['Ingredients']:
                print(f"Recipe '{recipe['Name']}' contains {ingredient_name}.")
                display_recipe(recipe)

file_name = str(input('Where is your data located? '))

try: 
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print('Error: file not found ')
else:
    search_ingredient(data)

