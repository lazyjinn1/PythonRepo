#Imports from sqlalchemy to allow us to use the ORM
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.orm import sessionmaker

#Connects us to our MySQL database
engine = create_engine("mysql://cf-python:password@localhost/task_database")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

#Main Class for our recipes
class Recipe(Base):
    #This creates our table
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    #Simplified representation of recipes
    def __repre__(self):
        return (f"{self.id} - {self.name} - {self.difficulty}")
    
    #Full representation of recipes
    def __str__(self):
        output = "\nRecipe Name: " + str(self.name) + \
            "\nCooking Time: " + str(self.cooking_time) + ' minutes'\
            "\nIngredients: " + str(self.ingredients) + \
            "\nDifficulty: " + str(self.difficulty)
        return output

    #Automatically returns our difficulty given cooking_time and numberOfIngredients
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
    
    #Used for returning the string "ingredients" as a list
    def return_ingredients_as_list(self):
        if self.ingredients == '':
            return self.ingredients
        else:
            return self.ingredients.split(', ')

#Runs our code to launch the table
Base.metadata.create_all(engine)

#Initializations for variables to be used in the methods below
all_ingredients = set()
all_recipes = session.query(Recipe).all()
all_ids = set()

def create_recipe():
    ingredientsArray = []
    print('==========================================')
    print('Thank you for adding a new recipe to the recipe list!')
    #Checks for variable type and value errors, otherwise it repeats
    while True:
        try:
            name = str(input("Name of Recipe: "))
            #Checks to make sure that the length is not too long or short
            if 0 >= len(name) or len(name) > 50:
                print("Invalid input!")
                continue
            else:
                break
        except ValueError:
            print("Invalid input. Please Enter a valid string.")

        except TypeError:
            print("Invalid input. Please Enter a valid string.")

    #Checks for variable type and value errors, otherwise it repeats
    while True:
        try:
            cooking_time = int(input("Cooking Duration (in minutes): "))
            break
        except ValueError:
            print("Invalid input. Please Enter a valid integer.")

        except TypeError:
            print("Invalid input. Please Enter a valid integer.")

    #Checks for variable type and value errors, otherwise it repeats
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
    #Continuously adds in ingredients to the soon-to-be ingredients list. User can choose to stop adding whenever.
    while True:
        try:
            while ingredient != '':
                ingredient = str(input("Add another ingredient or press 'Enter' to finish adding ingredients: "))
                ingredient_proper_case = ingredient.title() #This code is used a few times in the project and it simply sets the variable to Proper Case
                if ingredient != '':
                    ingredientsArray.append(ingredient_proper_case)
                continue
            break
        except ValueError:
            print("Invalid input. Please Enter a valid string.")

        except TypeError:
            print("Invalid input. Please Enter a valid string.")

    #Concatenates our list into a single string separated by ', '
    ingredients = ', '.join(str(ingredient) for ingredient in ingredientsArray)
    
    #difficulty is automatically calculated by this method
    difficulty = Recipe.calculate_difficulty(cooking_time, len(ingredientsArray))

    #defining our class to be entered into the database
    new_recipe = Recipe(
        name = name,
        ingredients = ingredients,
        cooking_time = cooking_time,
        difficulty = difficulty
    )
    
    #adding in new entry for database then commits the changes
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

        #appears quite often in this app. Simple choice for the user to do more or go back to the Main Menu
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
    # temporary id_list list that is used as a dummy array to input values into until they are ready to be put into all_ids
    temp_id_list = set()
    recipes_list = session.query(Recipe).all()
    # defines all_ids for us, which is useful for later portions
    for recipe in all_recipes:
        temp_id_list.add(recipe.id)
        for id in temp_id_list:
            all_ids.add(id)
    # if recipes_list is empty, then the user is shown this and given an option to add the first recipe
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
    # enumerate is used so that index can show the user number inputs for the respective recipe or ingredient
    for index, recipe in enumerate(recipes_list):
        print("Recipe #:", index+1, recipe.name)
    while True:
        try:
            response = int(input("Which recipe would you like to view? "))

            # this is where the all_ids is useful for. It checks to make sure that the response is not larger than the largest of all the ids that we have.
            if type(response) != int or response > max(all_ids) or response <= 0:
                print('Invalid choice, please try again.')
                continue
            else:
                #response is being subtracted by one because we added 1 to index earlier (just for readability - so 0 wasn't an option).
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
            # this searches in Recipe.ingredients and returns all the entries that have a match for the ingredient name.
            # % % surrounds ingredient name because ingredient_name that we're looking for is stored in a string. 
            # This lets us filter by something inside the string too.
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
    except ValueError:
        print('The chosen number is of an incorrect type. Chosen number needs to be an integer. . .')
        print('Returning to Main Menu. . . ')
        return
    
def update_recipe():
    print('==========================================')
    # all_recipes is fetched often in order to get up-to-date records.
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
                    # users are given the option to change anything, each with their own path to follow.
                    print('1 - Recipe Name:', recipe.name)
                    print('2 - Recipe Ingredients:', recipe.ingredients)
                    print('3 - Time to Make (in minutes):', recipe.cooking_time)
                    print('4 - Difficulty:', recipe.difficulty)
                    choice = int(input("What would you like to change? "))
                    # users may change the name of the recipe but will
                    if choice == 1:
                        while True:
                            try:
                                name_choice = str(input("New Recipe Name: "))
                                #Checks to make sure that the length is not too long or short
                                if 0 >= len(name_choice) or len(name_choice) > 50:
                                    print("Invalid input!")
                                    continue
                                else:
                                    break
                            except ValueError:
                                print("Invalid input. Please Enter a valid string.")
                                return
                            except TypeError:
                                print("Invalid input. Please Enter a valid string.")
                                return
                        #updates entry where the id matches
                        session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.name: name_choice})
                        session.commit()
                    elif choice == 2:
                        current_cooking_time = recipe.cooking_time
                        #gives the user the option on how they would like to update the ingredients list/string
                        add_or_change_ingredients = int(input("Would you like to 1:(Add Ingredients), 2:(Change All Ingredients) or 3:(Delete An Ingredient)? (1, 2 or 3): "))
                        if add_or_change_ingredients == 1:
                            ingredientsArray = recipe.ingredients.split(', ')
                            ingredient = str(input("Start by adding an ingredient: "))
                            ingredient_title = ingredient.title()
                            ingredientsArray.append(ingredient_title)
                            while ingredient != '':
                                ingredient = str(input("Add another ingredient or press 'Enter' to finish adding ingredients: "))
                                ingredient_title = ingredient.title()
                                if ingredient not in ingredientsArray:
                                    ingredientsArray.append(ingredient_title)
                                    numberOfIngredients = int(len(ingredientsArray))
                            ingredients_choice = ', '.join(str(ingredient) for ingredient in ingredientsArray)
                            #new difficulty is calculated to accomodate the change in number of ingredients
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
                            #new difficulty is calculated to accomodate the change in number of ingredients
                            new_difficulty = Recipe.calculate_difficulty(current_cooking_time, numberOfIngredients)
                            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.ingredients: ingredients_choice})
                            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: new_difficulty})
                            session.commit()
                        elif add_or_change_ingredients == 3:
                            ingredientsArray = recipe.ingredients.split(', ')
                            for index, ingredient in enumerate(ingredientsArray):
                                print(f'{index} - {ingredient}') 
                            #Takes in the index so that it can be used in the pop function
                            deleted_ingredient_index = int(input("Please choose the ingredient you wish to remove: "))
                            #Takes in the name so that it can be displayed even after deletion
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
                        try:
                            cooking_time_choice = int(input("New cooking time: "))
                        except ValueError:
                            print("Invalid input. Please Enter a valid string.")
                            return
                        except TypeError:
                            print("Invalid input. Please Enter a valid string.")
                            return
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
                    print('Time to Make:', recipe.cooking_time, 'minutes')
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
    # uses Temp List and all_ids for same purpose as before
    temp_id_list = set()
    all_recipes = session.query(Recipe).all()
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
                    # asks for confirmation for the recipe.
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
    print('==========================================')
    print('Thank you for using our application! We hope to see you next time!')
    session.commit()
    session.close()
    engine.close()
    exit()

#main menu for our program
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
