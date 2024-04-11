from django.db import models

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length = 20)
    note = models.TextField()

    def __str__(self):
        return str(self.ingredient_name)