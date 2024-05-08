from django import forms
from .models import Recipe

CHART_CHOICES = {
    ('bar', 'Bar Chart'),
    ('pie', 'Pie Chart'),
    ('line', 'Line Chart')
}

DIFFICULTY_CHOICES = (
    ('', 'All'),
    ('E', 'Easy'),
    ('M', 'Medium'),
    ('I', 'Intermediate'),
    ('H', 'Hard')
)

class SearchRecipeForm(forms.Form):
    recipe_name = forms.CharField(max_length = 120, required=False)
    ingredient = forms.CharField(max_length = 20, required=False)
    difficulty = forms.ChoiceField(choices = DIFFICULTY_CHOICES, required=False)
    max_cooking_time = forms.FloatField(required=False)
    min_cooking_time = forms.FloatField(required=False)

class DataVisualizationForm(forms.Form):
    chart_type = forms.ChoiceField(choices = CHART_CHOICES, required=False)

class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'ingredients', 'cooking_time', 'difficulty', 'pic', 'note', ]