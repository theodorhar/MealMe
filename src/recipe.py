import numpy as np
#needs access to recipes database for recipe lookup

class Recipe(object):
    def __init__(self,id:int,url:str,name:str,ingredients:np.array,directions:np.array,prep:int,cook:int,ready:int,calories:int):
        #'url', 'name', 'rating', 'ingredients', 'directions', 'prep', 'cook', 'ready in', 'calories'
        self._id = id
        self._url = url
        self._name = name
        self._ingredients = ingredients
        self._directions = directions
        self._prep = prep
        self._cook = cook
        self._ready = ready
        self._calories = calories
    def get_recipe_embedding(self,relevant_ingredients:np.array, recipe_id:int) -> np.array:
        favor = dict.fromkeys(relevant_ingredients,0)

        return np.fromiter(favor.values(), dtype=float)