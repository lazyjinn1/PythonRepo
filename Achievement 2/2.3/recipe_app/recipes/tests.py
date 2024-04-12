from django.test import TestCase
from .models import Recipe

class RecipeTests(TestCase):
    def setUpTestData():
        Recipe.objects.create(
            recipe_name = 'Egg and Mushroom Omelette',
            ingredients = 'Eggs, Salt, Butter, Mushrooms, Basil, Bell Peppers',
            cooking_time = 8.5,
            difficulty = 'Easy',
            note='This is the ingredient entry for Eggs, not the Recipe.'
        )
    
    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('recipe_name').verbose_name
        self.assertEqual(field_label, 'recipe name')

    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('recipe_name').max_length
        self.assertEqual(max_length, 50)

    def test_recipe_name_type(self):
        recipe = Recipe.objects.get(id=1)
        recipe_name_value = recipe.recipe_name
        self.assertIsInstance(recipe_name_value, str)

    def test_ingredients_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('ingredients').max_length
        self.assertEqual(max_length, 200)

    def test_ingredients_type(self):
        recipe = Recipe.objects.get(id=1)
        ingredients_value = recipe.ingredients
        self.assertIsInstance(ingredients_value, str)

    def test_ingredients_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('ingredients').max_length
        self.assertEqual(max_length, 200)

    def test_recipe_cooking_time(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('cooking_time')
        field_value = field_label.value_from_object(recipe)
        self.assertEqual(field_value, 8.5)
    
    def test_cooking_time_type(self):
        recipe = Recipe.objects.get(id=1)
        cooking_time_value = recipe.cooking_time
        self.assertIsInstance(cooking_time_value, float)

    def test_recipe_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('difficulty')
        field_value = field_label.value_from_object(recipe)
        self.assertEqual(field_value, 'Easy')

    def test_difficulty_type(self):
        recipe = Recipe.objects.get(id=1)
        difficulty_value = recipe.difficulty
        self.assertIsInstance(difficulty_value, str)

    def test_difficulty_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('difficulty').max_length
        self.assertEqual(max_length, 20)

    
