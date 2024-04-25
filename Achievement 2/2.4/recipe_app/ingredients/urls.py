from django.urls import path
from .views import ingredients

app_name = 'recipes'

urlpatterns = [
    path('', ingredients),
]