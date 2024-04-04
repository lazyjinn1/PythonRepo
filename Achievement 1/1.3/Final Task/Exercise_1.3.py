recipes_list = []
ingredients_list = []

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
    return dict(recipe)

numberOfRecipes = int(input("How many recipes would you like to input? "))

for n in range(0, numberOfRecipes): 
    recipe = take_recipe()
    for ele in recipe['Ingredients']:
        if ele not in ingredients_list:
            ingredients_list.append(ele)
            print('Updated Ingredients List: ', ingredients_list)
    recipes_list.append(recipe)
    print('Updated Recipes List: ', recipes_list)

for recipe in recipes_list:
    if recipe['Cooking Time'] < 10 and len(recipe['Ingredients']) < 4:
        difficulty = "Easy"
    elif recipe['Cooking Time'] < 10 and len(recipe['Ingredients']) >= 4:
        difficulty = "Medium"
    elif recipe['Cooking Time'] >= 10 and len(recipe['Ingredients']) < 4:
        difficulty = "Intermediate"
    elif recipe['Cooking Time'] >= 10 and len(recipe['Ingredients']) >= 4:
        difficulty = "Hard"
    print('Recipe: ', recipe['Name'])
    print('Cooking Time: ', recipe['Cooking Time'])
    print('Ingredients: ', recipe['Ingredients'])
    print('Difficulty: ', difficulty)
