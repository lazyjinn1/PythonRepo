from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://cf-python:password@localhost/my_database")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repre__(self):
        return (f"{self.id} - {self.name} - {self.difficulty}")
    
    def __str__(self):
        output = "\nRecipe Name: " + str(self.name) + \
            "\nCooking Time: " + str(self.cooking_time) + ' minutes'\
            "\nIngredients: " + str(self.ingredients) + \
            "\nDifficulty: " + str(self.difficulty)
        return output

    def calculate_difficulty(cooking_time, numberOfIngredients):
        if cooking_time < 10 and numberOfIngredients < 4:
            difficulty = 'Easy'
        elif cooking_time < 10 and numberOfIngredients >= 4:
            difficulty = 'Medium'
        elif cooking_time >= 10 and numberOfIngredients < 4:
            difficulty = 'Intermediate'
        elif cooking_time >= 10 and numberOfIngredients >= 4:
            difficulty = 'Hard'
        else:
            difficulty = ''
        return difficulty

Base.metadata.create_all(engine)

all_ingredients = set()
all_recipes = session.query(Recipe).all()
all_ids = set()
def create_recipe():
    ingredientsArray = []
    print('==========================================')
    print('Thank you for adding a new recipe to the recipe list!')
    while True:
        try:
            name = str(input("Name of Recipe: "))
            if 0 >= len(name) or len(name) > 50:
                print("Invalid input!")
                continue
            elif len(name) < 50:
                break
        except ValueError:
            print("Invalid input. Please Enter a valid string.")

        except TypeError:
            print("Invalid input. Please Enter a valid string.")

    while True:
        try:
            cooking_time = int(input("Cooking Duration (in minutes): "))
            break
        except ValueError:
            print("Invalid input. Please Enter a valid integer.")

        except TypeError:
            print("Invalid input. Please Enter a valid integer.")

    while True:
        try:
            ingredient = str(input("Start by adding an ingredient: "))
            break

        except ValueError:
            print("Invalid input. Please Enter a valid string.")

        except TypeError:
            print("Invalid input. Please Enter a valid string.")

    ingredient_proper_case = ingredient.title()
    ingredientsArray.append(ingredient_proper_case)
    while True:
        try:
            while ingredient != '':
                ingredient = str(input("Add another ingredient or press 'Enter' to finish adding ingredients: "))
                ingredient_proper_case = ingredient.title()
                if ingredient != '':
                    ingredientsArray.append(ingredient_proper_case)
                continue
            break
        except ValueError:
            print("Invalid input. Please Enter a valid string.")

        except TypeError:
            print("Invalid input. Please Enter a valid string.")

    ingredients = ', '.join(str(ingredient) for ingredient in ingredientsArray)
    
    difficulty = Recipe.calculate_difficulty(cooking_time, len(ingredientsArray))

    new_recipe = Recipe(
        name = name,
        ingredients = ingredients,
        cooking_time = cooking_time,
        difficulty = difficulty
    )
    
    session.add(new_recipe)
    session.commit()

    print(f'The recipe for {name} has been added to the Recipe List!')
    response = str(input('Type Y to view your recipe or press Enter to go back to the Main Menu: '))
    if response == 'Y' or response == 'y':
        print('=================')
        print(f'Recipe Name: {name}')
        print(f'Recipe Ingredients: {ingredients}')
        print(f'Time to Make (in minutes): {cooking_time}')
        print(f'Difficulty: {difficulty}')
        print('=================')
        response = str(input("Type Y to create more recipes or press Enter to go back to the Main Menu: "))
        if response == 'Y' or response == 'y':
            create_recipe()
        else:
            print('Returning to Main Menu. . . ')
            return
    else:
        print('Returning to Main Menu. . . ')
        return
        
    
def view_all_recipes():
    print('==========================================')
    recipes_list = session.query(Recipe).all()
    if len(recipes_list) <= 0:
        choice = str(input("Unfortunately, there are no recipes here. Type Y to create one or press Enter to return to the Main Menu.: "))
        if choice == 'Y' or choice == 'y':
            print('Redirecting to Add a Recipe. . .')
            create_recipe(session)
        elif choice == 'N' or choice == 'n':
            print('Returning to Main Menu. . . ')
            return
        else:
            print('Invalid response:')
            print('Returning to Main Menu. . . ')
            return
    for index, recipe in enumerate(recipes_list):
        print("Recipe #:", index+1, recipe.name)
    while True:
        try:
            response = int(input("Which recipe would you like to view? "))
            chosen_recipe = list(recipes_list)[response-1]
            print(f"Displaying recipe for {chosen_recipe.name}...")
            print(chosen_recipe)
            print('==========================================')
            break
        except ValueError:
            print("Invalid input. Please Enter a valid integer.")
            continue
        except TypeError:
            print("Invalid input. Please Enter a valid integer.")
            continue

    response = str(input("Type Y to view more recipes or press Enter to go back to the Main Menu: "))
    if response == 'Y' or response == 'y':
        view_all_recipes()
    else:
        print('Returning to Main Menu. . . ')
        return

def search_by_ingredients():
    print('==========================================')
    all_recipes = session.query(Recipe).all()
    if len(all_recipes) <= 0:
        response = input('Unfortunately, we have no ingredients here. Type Y to add your own recipe or press Enter to go back to the Main Menu: ')
        if response == 'Y' or response == 'y':
            print('Redirecting to Add a Recipe. . .')
            create_recipe()
        else:
            print('Returning to Main Menu. . .')
            return
    for recipe in all_recipes:
        ingredients_list = recipe.ingredients.split(', ')
        for ingredient in ingredients_list:
            all_ingredients.add(ingredient.title())
    print('Search by ingredient: ')
    print('=================')
    all_ingredients_sorted = sorted(all_ingredients)
    for index, ingredient in enumerate(all_ingredients_sorted):
        print(f"{index+1}. {ingredient}")
    try:
        search_ingredient = int(input('Choose an ingredient (by number): '))
        print('=================')
        if 0 < search_ingredient <= len(all_ingredients_sorted):
            ingredient_name = list(all_ingredients_sorted)[search_ingredient-1]
            print('You have chosen: ', ingredient_name)
            found_recipes = session.query(Recipe).filter(Recipe.ingredients.like(f"%{ingredient_name}%")).all()
            number_of_found_recipes = len(found_recipes)
            print(f"{number_of_found_recipes} recipes found. . .")
            print('=================')
            for index, recipe in enumerate(found_recipes):
                print(f"{index+1} - {recipe.name}")
            try:
                search_input = int(input("Which would you like to view? "))
                search_index = search_input - 1
                recipe_chosen = found_recipes[search_index]
                print('=================')
                print('Recipe Name:', recipe_chosen.name)
                print('Recipe Ingredients:', recipe_chosen.ingredients)
                print('Time to Make (in minutes):', recipe_chosen.cooking_time)
                print('Difficulty:', recipe_chosen.difficulty)
                response = str(input("Type Y to search for more recipes or press Enter to go back to the Main Menu: "))
                if response == 'Y' or response == 'y':
                    search_by_ingredients()
                else:
                    print('Returning to Main Menu. . . ')
                    return
            except TypeError:
                print('The chosen number is of an incorrect type. Chosen number needs to be an integer. . .')
                print('Returning to Main Menu. . . ')
                return
        else:
            print('Invalid ingredient number. ')
            return
    except TypeError:
        print('The chosen number is of an incorrect type. Chosen number needs to be an integer. . .')
        print('Returning to Main Menu. . . ')
        return
    
def update_recipe():
    print('==========================================')
    all_recipes = session.query(Recipe).all()
    if len(all_recipes) <= 0:
        response = input('Unfortunately, we have no recipes here. Type Y to add one in or press Enter to return to the Main Menu.: ')
        if response == 'Y' or response == 'y':
            print('Redirecting to Add a Recipe. . .')
            create_recipe()
        else:
            print('Returning to Main Menu. . .')
            return
    else:
        for index, recipe in enumerate(all_recipes):
            print(index+1, "-", recipe.name)
        search_recipe = int(input("Please select a number to update: "))
        try: 
            if 0 < (search_recipe) <= len(all_recipes):
                recipe_id = all_recipes[search_recipe-1].id
                print('You have chosen ID: ', search_recipe)
                recipe = session.query(Recipe).filter(Recipe.id == recipe_id).one()
                print('=================')
                try:
                    print('1 - Recipe Name:', recipe.name)
                    print('2 - Recipe Ingredients:', recipe.ingredients)
                    print('3 - Time to Make (in minutes):', recipe.cooking_time)
                    print('4 - Difficulty:', recipe.difficulty)
                    choice = int(input("What would you like to change? "))
                    if choice == 1:
                        try:
                            name_choice = str(input("New name: "))
                        except TypeError:
                            print('The new name chosen is invalid. . .')
                            print('Returning to Main Menu. . . ')
                            return
                        except ValueError:
                            print('The new name chosen is invalid. . .')
                            print('Returning to Main Menu. . . ')
                            return
                        session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.name: name_choice})
                        session.commit()
                    elif choice == 2:
                        current_cooking_time = recipe.cooking_time
                        add_or_change_ingredients = int(input("Would you like to 1:(Add Ingredients), 2:(Change All Ingredients) or 3:(Delete An Ingredient)? (1, 2 or 3): "))
                        if add_or_change_ingredients == 1:
                            ingredientsArray = recipe.ingredients.split(', ')
                            ingredient = str(input("Start by adding an ingredient: "))
                            ingredient_title = ingredient.title()
                            ingredientsArray.append(ingredient_title)
                            while ingredient != '':
                                ingredient = str(input("Add another ingredient or press 'Enter' to finish adding ingredients: "))
                                ingredient_title = ingredient.title()
                                if ingredient != '':
                                    ingredientsArray.append(ingredient_title)
                                    numberOfIngredients = int(len(ingredientsArray))
                            ingredients_choice = ', '.join(str(ingredient) for ingredient in ingredientsArray)
                            new_difficulty = Recipe.calculate_difficulty(current_cooking_time, numberOfIngredients)
                            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.ingredients: ingredients_choice})
                            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: new_difficulty})
                            session.commit()
                        elif add_or_change_ingredients == 2:
                            ingredientsArray = []
                            ingredient = str(input("Start by adding an ingredient: "))
                            ingredient_title = ingredient.title()
                            ingredientsArray.append(ingredient_title)
                            while ingredient != '':
                                ingredient = str(input("Add another ingredient or press 'Enter' to finish adding ingredients: "))
                                ingredient_title = ingredient.title()
                                if ingredient != '':
                                    ingredientsArray.append(ingredient_title)
                                    numberOfIngredients = int(len(ingredientsArray))
                            ingredients_choice = ', '.join(str(ingredient) for ingredient in ingredientsArray)
                            new_difficulty = Recipe.calculate_difficulty(current_cooking_time, numberOfIngredients)
                            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.ingredients: ingredients_choice})
                            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: new_difficulty})
                            session.commit()
                        elif add_or_change_ingredients == 3:
                            ingredientsArray = recipe.ingredients.split(', ')
                            for index, ingredient in enumerate(ingredientsArray):
                                print(f'{index} - {ingredient}') 
                            deleted_ingredient_index = int(input("Please choose the ingredient you wish to remove: "))
                            deleted_ingredient_name = ingredientsArray[deleted_ingredient_index]
                            ingredientsArray.pop(deleted_ingredient_index)
                            numberOfIngredients = int(len(ingredientsArray))
                            ingredients_choice = ', '.join(str(ingredient) for ingredient in ingredientsArray)
                            new_difficulty = Recipe.calculate_difficulty(current_cooking_time, numberOfIngredients)
                            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.ingredients: ingredients_choice})
                            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: new_difficulty})
                            print(f'{deleted_ingredient_name} has been successfully deleted.')
                            session.commit()
                        else:
                            print('Invalid choice. ')
                            print('Returning to Main Menu. . . ')
                            return
                        
                    elif choice == 3:
                        ingredientsArray = recipe.ingredients.split(', ')
                        cooking_time_choice = int(input("New cooking time: "))
                        session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.cooking_time: cooking_time_choice})
                        session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: new_difficulty})
                        session.commit()
                    elif choice == 4:
                        try:
                            print('=================')
                            print(f'1 - Easy')
                            print(f'2 - Medium')
                            print(f'3 - Intermediate')
                            print(f'4 - Hard')
                            difficulty_input = int(input("Please choose a new difficulty: "))
                            if difficulty_input == 1:
                                difficulty_choice = 'Easy'
                                session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: difficulty_choice})
                                session.commit()
                            elif difficulty_input == 2:
                                difficulty_choice = 'Medium'
                                session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: difficulty_choice})
                                session.commit()
                            elif difficulty_input == 3:
                                difficulty_choice = 'Intermediate'
                                session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: difficulty_choice})
                                session.commit()
                            elif difficulty_input == 4:
                                difficulty_choice = 'Hard'
                                session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: difficulty_choice})
                                session.commit()
                            else:
                                print('Invalid difficulty number. ')
                                print('Returning to Main Menu. . . ')
                                return
                        except ValueError:
                            print('That choice is invalid, please try again: ')
                            print('Returning to Main Menu. . . ')
                            return
                        except TypeError:
                            print('The chosen number is of an incorrect type. It needs to be an integer')
                            print('Returning to Main Menu. . . ')
                            return   
                except ValueError:
                    print('That choice is invalid, please try again: ')
                    print('Returning to Main Menu. . . ')
                    return
                except TypeError:
                    print('The chosen number is of an incorrect type. It needs to be an integer')
                    print('Returning to Main Menu. . . ')
                    return
                finally:
                    recipe = session.query(Recipe).filter(Recipe.id == recipe_id).one()
                    print('=================')
                    print('Recipe Name:',recipe.name)
                    print('Recipe Ingredients:', recipe.ingredients)
                    print('Time to Make (in minutes):', recipe.cooking_time)
                    print('Difficulty:', recipe.difficulty)
                    print('Returning to Main Menu. . . ')
                    return
            else:
                print('Invalid recipe number. ')
                print('Returning to Main Menu. . . ')
                return
        except ValueError:
            print('The chosen number is of an incorrect type. It needs to be an integer')
            print('Returning to Main Menu. . . ')
            return
        
def delete_recipe():
    print('==========================================')
    temp_id_list = set()
    for recipe in all_recipes:
        temp_id_list.add(recipe.id)
        for id in temp_id_list:
            all_ids.add(id)
    if len(all_recipes) <= 0:
        response = input('Unfortunately, we have no recipes here. Type Y to add one in or press Enter to return to the Main Menu: ')
        if response == 'Y' or response == 'y':
            print('Redirecting to Add a Recipe. . .')
            create_recipe()
        else:
            print('Returning to Main Menu. . .')
            return
    for recipe in all_recipes:
        print("ID: ", recipe.id, "- ", recipe.name)

    while True:
        try:
            delete_recipeID = int(input("Please select the recipe ID that you wish to delete: "))
            if delete_recipeID < 0 or delete_recipeID > max(all_ids):
                print('Invalid ID. Try again.')
                continue
            try:
                recipe_deleted_to_be = session.query(Recipe).filter(Recipe.id == delete_recipeID).one()
                delete_recipe_name = recipe_deleted_to_be.name
                try:
                    confirmation = str(input(f"Are you sure you want to delete {delete_recipe_name}? Type Y to confirm to press Enter to cancel."))
                    if confirmation == 'Y' or confirmation == 'y':
                        session.delete(recipe_deleted_to_be)
                        session.commit()
                        print(f'Deleting recipe ID #: {delete_recipeID}. . .')
                        print(f'The recipe for {delete_recipe_name} has been successfully deleted.')
                        try:
                            response = str(input("Type Y to delete more recipes or press Enter to return to the Main Menu. "))
                            if response == 'Y' or response == 'y':
                                delete_recipe()
                            else:
                                print('Returning to Main Menu. . . ')
                                return
                        except ValueError:
                            print("Invalid input. Please Enter a valid string.")
                        except TypeError:
                            print("Invalid input. Please Enter a valid string.")
                except ValueError:
                        print("Invalid input. Please Enter a valid string.")
                except TypeError:
                        print("Invalid input. Please Enter a valid string.")
            except ValueError:
                print("Invalid input. Please Enter a valid ID.")
            except TypeError:
                print("Invalid input. Please Enter a valid ID.")
        except ValueError:
            print("Invalid input. Please Enter a valid integer.")
        except TypeError:
            print("Invalid input. Please Enter a valid integer.")

def exit_program():
    session.commit()
    session.close()
    engine.close()
    exit()

def main_menu():
    print('==========================================')
    print("What would you like to do? Type 'quit' to exit program.")
    print('1. Create a recipe')
    print('2. View all recipes')
    print('3. Search by ingredient')
    print('4. Update a recipe')
    print('5. Delete a recipe')

main_menu()
choice = input("Your choice: ")

while choice != 'quit':
    if choice == '1':
        create_recipe()
    elif choice == '2':
        view_all_recipes()
    elif choice == '3':
        search_by_ingredients()
    elif choice == '4':
        update_recipe()
    elif choice == '5':
        delete_recipe()
    elif choice == 'quit':
        exit_program()
    else:
        print("Invalid choice. Please choose again.")
    main_menu()
    choice = input("Choose again: ")
