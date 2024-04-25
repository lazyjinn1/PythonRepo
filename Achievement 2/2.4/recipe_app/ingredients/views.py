from django.shortcuts import render

def ingredients(request):
    return render(request, 'ingredients/ingredients_home.html')