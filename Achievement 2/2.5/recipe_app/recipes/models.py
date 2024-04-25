from django.db import models
from django.shortcuts import reverse

class Choices:
    difficulty_choices = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('I', 'Intermediate'),
        ('H', 'Hard')
    )


class Recipe(models.Model):
    recipe_name = models.CharField(max_length = 50)
    ingredients = models.CharField(max_length = 200)
    cooking_time = models.FloatField(help_text='in minutes')
    difficulty = models.CharField(max_length = 15, choices=Choices().difficulty_choices, default='E')
    pic = models.ImageField(upload_to='recipes', default='no-picture.jpg')
    note = models.TextField(blank=True)

    def __str__(self):
        return str(self.recipe_name)
    
    def get_absolute_url(self):
       return reverse('recipes:detail', kwargs={'pk': self.pk})