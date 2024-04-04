class Recipe(object):
    all_ingredients = []
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = ''

    def get_name(self):
        return self.name
    
    def get_cooking_time(self):
        return self.cooking_time
    
    def set_name(self, name):
        self.name = name

    def set_cooking_time(self, cooking_time):
        self.cooking_time = int(cooking_time)
        self.calculate_difficulty()

    def add_ingredients(self, *ingredient_list):
        for ingredient in ingredient_list:
            if ingredient not in self.ingredients:
                self.ingredients.append(ingredient)
            elif ingredient in self.ingredients:
                print(f'{ingredient} is already in your ingredient list.')
        self.update_all_ingredients()
        self.calculate_difficulty()

    def get_ingredients(self):
        return self.ingredients

    def get_difficulty(self):
        return self.difficulty

    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Hard'
        elif not self.cooking_time or not self.ingredients:
            self.difficulty = ''
    
    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        elif ingredient not in self.ingredients:
            return False
        
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in self.all_ingredients:
                self.all_ingredients.append(ingredient)
    
    def __str__(self):
        output = "\nRecipe Name: " + str(self.name) + \
            "\nCooking Time: " + str(self.cooking_time) + ' minutes'\
            "\nIngredients: " + str(self.ingredients) + \
            "\nDifficulty: " + str(self.difficulty)
        return output
    
    def recipe_search(self, data, *search_term):
        for recipe in data:
            for ingredient in search_term:
                result = self.search_ingredient(ingredient)
                if(result == True):
                    print(recipe)
                elif(result == False):
                    print('Ingredient was not found in any recipe')

tea = Recipe('Tea')
tea.add_ingredients('Tea Leaves', 'Sugar', 'Water')
tea.set_cooking_time(5)

coffee = Recipe('Coffee')
coffee.add_ingredients('Coffee Powder', 'Sugar', 'Water')
coffee.set_cooking_time(5)

cake = Recipe('Cake')
cake.add_ingredients('Sugar', 'Butter', 'Eggs', 'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk')
cake.set_cooking_time(50)

banana_smoothie = Recipe('Banana Smoothies')
banana_smoothie.add_ingredients('Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes')
banana_smoothie.set_cooking_time(5)

recipe_list = [tea, coffee, cake, banana_smoothie]
search_terms = ['Water', 'Sugar', 'Tea Leaves']

for search_term in search_terms:
    for recipe in recipe_list:
        result = recipe.search_ingredient(search_term)
        if result == True:
            print(f'{search_term} found in {recipe.name}')
            print(recipe, '\n')
        if result == False:
            print(f'{search_term} not found in {recipe.name}\n')
