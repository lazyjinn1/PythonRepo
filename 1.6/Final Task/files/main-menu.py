import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password',
    database='task_database')

cursor = conn.cursor()

all_ingredients = set()
all_recipes = set()

def create_recipe(conn, cursor):
    ingredientsArray = []
    print('==========================================')
    print('Thank you for adding a new recipe to the recipe list!')
    name = input("Name of Recipe: ")
    cooking_time = int(input("Cooking Duration (in minutes): "))
    ingredient = str(input("Start by adding an ingredient: "))
    ingredient_title = ingredient.title()
    ingredientsArray.append(ingredient_title)
    while ingredient != '':
        ingredient = str(input("Add another ingredient or press 'Enter' to finish adding ingredients: "))
        ingredient_title = ingredient.title()
        if ingredient != '':
            ingredientsArray.append(ingredient_title)
    ingredients = ', '.join(str(ingredient) for ingredient in ingredientsArray)
    difficulty = calculate_difficulty(cooking_time, len(ingredientsArray))
    sql = "INSERT INTO Recipes(name, ingredients, cooking_time, difficulty) VALUES(%s, %s, %s, %s)"
    val = (name, ingredients, cooking_time, difficulty)
    cursor.execute(sql, val)
    conn.commit()
    print(f'The recipe for {name} has been added to the Recipe List!')
    response = str(input('Would you like to view your new recipe? Y/N: '))
    if response == 'Y':
        print('=================')
        print(f'Recipe Name: {name}')
        print(f'Recipe Ingredients: {ingredients}')
        print(f'Time to Make (in minutes): {cooking_time}')
        print(f'Difficulty: {difficulty}')
        print('Returning to Main Menu. . . ')
        return
    else:
        print('Returning to Main Menu. . . ')
        return

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

def search_recipe(conn, cursor):
    print('==========================================')
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    for row in results:
        newIngredientArray = row[0].split(', ')
        for ingredient in newIngredientArray:
            if ingredient not in all_ingredients:
                title_case_ingredient = ingredient.title()
                all_ingredients.add(title_case_ingredient)
    print('Search by ingredient: ')
    all_ingredients_sorted = sorted(all_ingredients)
    for index, ingredient in enumerate(all_ingredients_sorted):
        print(f"{index+1}. {ingredient}")
    try:
        search_ingredient = int(input('Choose an ingredient (by number): '))
        print('=================')
        if 0 < search_ingredient <= len(all_ingredients_sorted):
            ingredient_name = list(all_ingredients_sorted)[search_ingredient-1]
            print('You have chosen: ', ingredient_name)
            sql = f"SELECT * FROM Recipes WHERE ingredients LIKE '%{ingredient_name}%'"
            cursor.execute(sql)
            found_recipes = cursor.fetchall()
            number_of_found_recipes = len(found_recipes)
            print(f"{number_of_found_recipes} recipes found. . .")
            print('=================')
            for index, recipe in enumerate(found_recipes):
                print(f"{index+1} - {recipe[1]}")
            search_input = int(input("Which would you like to view? "))
            search_index = search_input - 1
            print('=================')
            print(f'Recipe Name: {found_recipes[search_index][1]}')
            print(f'Recipe Ingredients: {found_recipes[search_index][2]}')
            print(f'Time to Make (in minutes): {found_recipes[search_index][3]}')
            print(f'Difficulty: {found_recipes[search_index][4]}')
            print('Returning to Main Menu. . . ')
        else:
            print('Invalid ingredient number. ')
            return
    except TypeError:
        print('The chosen number is of an incorrect type. It needs to be an integer')
        print('Returning to Main Menu. . . ')
        return

def update_recipe(conn, cursor):
    print('==========================================')
    cursor.execute("SELECT * FROM Recipes")
    all_recipes = cursor.fetchall()
    if len(all_recipes) <= 0:
        response = input('Unfortunately, we have no recipes here. Would you care to add one in? Y/N: ')
        if response == 'Y':
            print('Redirecting to Add a Recipe. . .')
            create_recipe(conn, cursor)
        elif response ==  'N':
            print('Returning to Main Menu. . .')
            return
    else:
        for index, recipe in enumerate(all_recipes):
            print(index+1, "-", recipe[1])
        search_recipe = int(input("Please select a number to update: "))
        try: 
            if 0 < (search_recipe) <= len(all_recipes):
                recipe_id = all_recipes[search_recipe-1][0]
                print('You have chosen ID: ', search_recipe)
                sql = f"SELECT * FROM Recipes WHERE id = {recipe_id}"
                cursor.execute(sql)
                recipe = cursor.fetchone()
                print('=================')
                try:
                    print(f'1 - Recipe Name: {recipe[1]}')
                    print(f'2 - Recipe Ingredients: {recipe[2]}')
                    print(f'3 - Time to Make (in minutes): {recipe[3]}')
                    print(f'4 - Difficulty: {recipe[4]}')
                    choice = int(input("What would you like to change? "))
                    if choice == 1:
                        name_choice = str(input("New name: "))
                        sql = "UPDATE Recipes SET name = %s WHERE id = %s"
                        cursor.execute(sql, (name_choice, recipe_id))
                        conn.commit()
                    elif choice == 2:
                        current_cooking_time = recipe[3]
                        add_or_change_ingredients = int(input("Would you like to 1:(Add Ingredients), 2:(Change All Ingredients) or 3:(Delete An Ingredient)? (1, 2 or 3): "))
                        if add_or_change_ingredients == 1:
                            ingredientsArray = recipe[2].split(', ')
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
                            new_difficulty = calculate_difficulty(current_cooking_time, numberOfIngredients)
                            sql1 = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
                            cursor.execute(sql1, (ingredients_choice, recipe_id))
                            sql2 = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
                            cursor.execute(sql2, (new_difficulty, recipe_id))
                            conn.commit()
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
                            new_difficulty = calculate_difficulty(current_cooking_time, numberOfIngredients)
                            sql1 = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
                            cursor.execute(sql1, (ingredients_choice, recipe_id))
                            sql2 = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
                            cursor.execute(sql2, (new_difficulty, recipe_id))
                            conn.commit()
                        elif add_or_change_ingredients == 3:
                            ingredientsArray = recipe[2].split(', ')
                            for index, ingredient in enumerate(ingredientsArray):
                                print(f'{index} - {ingredient}') 
                            deleted_ingredient_index = int(input("Please choose the ingredient you wish to remove: "))
                            deleted_ingredient_name = ingredientsArray[deleted_ingredient_index]
                            ingredientsArray.pop(deleted_ingredient_index)
                            numberOfIngredients = int(len(ingredientsArray))
                            ingredients_choice = ', '.join(str(ingredient) for ingredient in ingredientsArray)
                            new_difficulty = calculate_difficulty(current_cooking_time, numberOfIngredients)
                            sql1 = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
                            cursor.execute(sql1, (ingredients_choice, recipe_id))
                            sql2 = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
                            cursor.execute(sql2, (new_difficulty, recipe_id))
                            print(f'{deleted_ingredient_name} has been successfully deleted.')
                            conn.commit()
                        else:
                            print('Invalid choice. ')
                            print('Returning to Main Menu. . . ')
                            return
                        
                    elif choice == 3:
                        ingredientsArray = recipe[2].split(', ')
                        cooking_time_choice = int(input("New cooking time: "))
                        sql2 = "UPDATE Recipes SET cooking_time = %s WHERE id = %s"
                        cursor.execute(sql2, (cooking_time_choice, recipe_id))
                        new_difficulty = calculate_difficulty(cooking_time_choice, len(ingredientsArray))
                        sql3 = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
                        cursor.execute(sql3, (new_difficulty, recipe_id))
                        conn.commit()
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
                                sql = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
                                cursor.execute(sql, (difficulty_choice, recipe_id))
                                conn.commit()
                            elif difficulty_input == 2:
                                difficulty_choice = 'Medium'
                                sql = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
                                cursor.execute(sql, (difficulty_choice, recipe_id))
                                conn.commit()
                            elif difficulty_input == 3:
                                difficulty_choice = 'Intermediate'
                                sql = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
                                cursor.execute(sql, (difficulty_choice, recipe_id))
                                conn.commit()
                            elif difficulty_input == 4:
                                difficulty_choice = 'Hard'
                                sql = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
                                cursor.execute(sql, (difficulty_choice, recipe_id))
                                conn.commit()
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
                    sql = f"SELECT * FROM Recipes WHERE id = {recipe_id}"
                    cursor.execute(sql)
                    recipe = cursor.fetchone()
                    print('=================')
                    print(f'Recipe Name: {recipe[1]}')
                    print(f'Recipe Ingredients: {recipe[2]}')
                    print(f'Time to Make (in minutes): {recipe[3]}')
                    print(f'Difficulty: {recipe[4]}')
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

def delete_recipe(conn, cursor):
    print('==========================================')
    sql = "SELECT * FROM Recipes"
    cursor.execute(sql)
    all_recipes = cursor.fetchall()
    for recipe in all_recipes:
        print("ID:", recipe[0], "-", recipe[1])
    delete_recipeID = int(input("Please select the recipe ID that you wish to delete: "))
    sql1 = f"SELECT * FROM Recipes WHERE id = {delete_recipeID}"
    cursor.execute(sql1)
    delete_recipe = cursor.fetchone()
    delete_recipe_name = delete_recipe[1]
    sql2 = f"DELETE FROM Recipes WHERE id = {delete_recipeID}"
    cursor.execute(sql2)
    conn.commit()
    print(f'Deleting recipe ID #: {delete_recipeID}. . .')
    print(f'{delete_recipe_name} has been successfully deleted.')
    print('Returning to Main Menu. . . ')
    return

def exit_program(conn):
    conn.commit()
    conn.close()
    exit()

def main_menu():
    print('==========================================')
    print("What would you like to do? Type 'quit' to exit program.")
    print('1. Create a recipe')
    print('2. Search for a recipe')
    print('3. Update a recipe')
    print('4. Delete a recipe')

main_menu()
choice = input("Your choice: ")

while choice != 'quit':
    if choice == '1':
        create_recipe(conn, cursor)
    elif choice == '2':
        search_recipe(conn, cursor)
    elif choice == '3':
        update_recipe(conn, cursor)
    elif choice == '4':
        delete_recipe(conn, cursor)
    elif choice == 'quit':
        exit_program(conn)
    else:
        print("Invalid choice. Please choose again.")
    main_menu()
    choice = input("Your choice: ")
