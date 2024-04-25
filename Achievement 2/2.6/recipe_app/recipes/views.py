from django.views.generic import ListView, DetailView
from .models import Recipe
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):                     
   model = Recipe                                        
   template_name = 'recipes/recipes_detail.html'  