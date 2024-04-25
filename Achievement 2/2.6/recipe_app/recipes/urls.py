from django.urls import path
from .views import RecipeListView, RecipeDetailView

app_name = 'recipes'

urlpatterns = [
    path('home', RecipeListView.as_view(), name='home'),
    path('<pk>', RecipeDetailView.as_view(), name='detail')
]