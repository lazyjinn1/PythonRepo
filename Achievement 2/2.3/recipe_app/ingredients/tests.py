from django.test import TestCase
from .models import Ingredient

class IngredientTests(TestCase):
    def setUpTestData():
        Ingredient.objects.create(
            ingredient_name='Eggs',
            note='This is the ingredient entry for Eggs, not the Recipe.'
        )
    
    def test_ingredient_name(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('ingredient_name').verbose_name
        self.assertEqual(field_label, 'ingredient name')

    def test_ingredient_name_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('ingredient_name').max_length
        self.assertEqual(max_length, 20)
