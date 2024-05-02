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
    recipe_name = models.CharField(max_length = 50, verbose_name='Recipe Name')
    ingredients = models.CharField(max_length = 200, verbose_name='Ingredients')
    cooking_time = models.FloatField(help_text='in minutes', verbose_name='Cooking Time')
    difficulty = models.CharField(max_length=15, choices=Choices().difficulty_choices, default='E')
    pic = models.ImageField(upload_to='recipes', default='no-picture.jpg', blank=True, null=True)
    note = models.TextField(blank=True, verbose_name='Note')

    def __str__(self):
        return self.recipe_name

    
    def get_absolute_url(self):
       return reverse('recipes:detail', kwargs={'pk': self.pk})
