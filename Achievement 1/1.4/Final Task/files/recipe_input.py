import pickle

recipes_list = []
ingredients_list = []

def calc_difficulty(recipe):
    if recipe['Cooking Time'] < 10 and len(recipe['Ingredients']) < 4:
        difficulty = "Easy"
    elif recipe['Cooking Time'] < 10 and len(recipe['Ingredients']) >= 4:
        difficulty = "Medium"
    elif recipe['Cooking Time'] >= 10 and len(recipe['Ingredients']) < 4:
        difficulty = "Intermediate"
    elif recipe['Cooking Time'] >= 10 and len(recipe['Ingredients']) >= 4:
        difficulty = "Hard"
    recipe['Difficulty'] = difficulty
 
def take_recipe():
    ingredients = []
    name = str(input("What is the name of your recipe? "))
    cooking_time = float(input("How long does your recipe take to make (in minutes)? "))
    numberOfIngredients = int(input("How many ingredients does your recipe require? "))
    for i in range(0, numberOfIngredients):
        ingredient = str(input("Add an ingredient: "))
        ingredients.append(ingredient)
    recipe = {
        'Name': name,
        'Cooking Time': cooking_time,
        'Ingredients': ingredients
    }
    calc_difficulty(recipe)
    return recipe

filename = input('Enter a file name here: ')

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        recipes_list = data['recipes_list']
        ingredients_list = data['ingredients_list']
    
except FileNotFoundError:
    print('File does not exist - exiting, please try again later')
except:
    print('An unexpected error occurred. File might be empty')
else:
    file.close()
finally:
    print('Moving on to Recipes')

numberOfRecipes = int(input("How many recipes would you like to input? "))

for n in range(0, numberOfRecipes): 
    recipe = take_recipe()
    for ele in recipe['Ingredients']:
        if ele not in ingredients_list:
            ingredients_list.append(ele)
    recipes_list.append(recipe)

data = {
    'recipes_list': recipes_list,
    'ingredients_list': ingredients_list
}

with open(filename, 'wb') as file:
    pickle.dump(data, file)

print('Updated recipes:', recipes_list)
print('Updated ingredients:', ingredients_list)