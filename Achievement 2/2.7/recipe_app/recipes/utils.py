from recipes.models import Recipe
from io import BytesIO 
import base64
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

cooking_time_range = [0.0, 25.0, 50.0, 75.0, 100.0]
difficulty_names = {
    'E': 'Easy',
    'M': 'Medium',
    'I': 'Intermediate',
    'H': 'Hard'
}

def get_all_ingredients():
     all_ingredients = []
     recipes = Recipe.objects.all()
     for recipe in recipes:
          ingredients = recipe.ingredients.split(",")
          for ingredient in ingredients:
               ingredient = ingredient.strip()
               if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)
     return all_ingredients

def get_graph():
    buffer = BytesIO() #create a BytesIO buffer for the image     
    plt.savefig(buffer, format='png') #create a plot with a bytesIO object as a file-like object. Set format to png
    buffer.seek(0) #set cursor to the beginning of the stream
    image_png = buffer.getvalue() #retrieve the content of the file
    graph = base64.b64encode(image_png) #encode the bytes-like object
    graph = graph.decode('utf-8') #decode to get the string as output
    buffer.close() #free up the memory of buffer
    return graph #return the image/graph

def get_chart(chart_type, data, all_ingredients, **kwargs):
   plt.switch_backend('AGG')

   #specify figure size
   fig, ax = plt.subplots(figsize=(11,5))
   
   #select chart_type based on user input from the form
   if chart_type == 'line':
        plt.title("Distribution of Recipes by Ingredient")
        ingredients_count = {}
        recipes = Recipe.objects.all()
        for recipe in recipes:
            ingredients = recipe.ingredients.split(", ")
            for ingredient in ingredients:
                if ingredient not in ingredients_count:
                    ingredients_count[ingredient] = 0
                ingredients_count[ingredient] += 1
                
        sorted_ingredients = sorted(ingredients_count.keys())
        print(sorted_ingredients)
        
        x = np.arange(len(all_ingredients))
        y = [ingredients_count.get(ingredient, 0) for ingredient in all_ingredients]
        ax.plot(x, y, "or-", markersize=4)
        ax.set_xticks(x)
        ax.set_xticklabels(sorted_ingredients, rotation=90)
        ax.set_ylabel('Recipe Count')

   elif chart_type == 'pie':
        plt.title("Distribution of Recipes by Difficulty")
        difficulty_counts = data['difficulty'].value_counts()
        difficulty_counts.index = difficulty_counts.index.map(difficulty_names) 
        labels = difficulty_counts.index
        values = difficulty_counts.values
        
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')

   elif chart_type == 'bar':
        plt.title("Cooking Time by Recipe")
        ax.bar(data['recipe_name'], data['cooking_time'])
        ax.set_xticklabels(data['recipe_name'], rotation=50)
        ax.set_yticks(data['cooking_time'])
   else:
        print ('unknown chart type')

   #specify layout details
   plt.tight_layout()

   #render the graph to file
   chart = get_graph() 
   return chart       
