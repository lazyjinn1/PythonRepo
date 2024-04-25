from django.db import models

class Recipe(models.Model):
    recipe_name = models.CharField(max_length = 50)
    ingredients = models.CharField(max_length = 200)
    cooking_time = models.FloatField(help_text='in minutes')
    difficulty = models.CharField(max_length = 20)
    note = models.TextField(blank=True)

    def __str__(self):
        return str(self.recipe_name)