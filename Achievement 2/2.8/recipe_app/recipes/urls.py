from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('home', views.RecipeListView.as_view(), name='home'),
    path('search', views.search_view, name='recipes_search'),
    path('analytics', views.charts_view, name='charts_search'),
    path('create', views.create_recipe, name ='create_recipe'),
    path('<pk>', views.RecipeDetailView.as_view(), name='detail')
]