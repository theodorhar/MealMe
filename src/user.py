import numpy as np
import pandas as pd
import collections
#needs access to: current recipes database to fetch recipes
class User(object):
    def __init__(self):
        self._age = None
        self._name = None
        self._location = None
        self._id = None
        self._recipes_viewed = np.array([])
        self._recipes_made = np.array([])  #if it is in made it must be in viewed
        self._recipes_liked = np.array([]) #if it is in liked it must be in viewed
        self._ingredients_owned = collections.defaultdict(lambda : 0)
        self._weight_matrix = np.array([2,2,1,5]) #like,made,view,own weights in order
    def set_age(self,age:int) -> None:
        if type(age) != int:
            raise TypeError("type must be int- type: ",type(age))
        if age < 0:
            raise ValueError("age must be above 0- age:" ,age)
        self._age = age
    def set_name(self,name:str) -> None:
        self._name = name
    def set_id(self,id:int) -> None:
        if type(id) != int:
            raise TypeError("type must be int- type: ",type(id))
        self._int = id
    
    def add_like(self,id:int) -> None:
        np.append(self._recipes_liked,id)
    def add_view(self,id:int) -> None:
        np.append(self._recipes_viewed,id)
    def add_make(self,id:int) -> None:
        np.append(self._recipes_made,id)
    def update_ingredients(self,food:dict) -> None:
        for x,count in food.items():
            self._ingredients_owned[x] += count
    def update_weight_matrix(self,weights:list) -> None:
        self._weight_matrix = weights
    
    #given a list of top ingredients, return a dict that measures favorability of certain ingredients (0-1)
    #uses inverse tan function to map 0-infinity to 0-1
    #eg [corn,garlic] = [0.1,0.9]
    def get_favorability_array(self,relevant_ingredients: list,recipes:pd.Series) -> np.array:
        favor = dict.fromkeys(relevant_ingredients,0)
        tanfunc = lambda x: np.arctan(x)/ (np.pi/2)
        for recipe in self._recipes_liked:
            for ing in recipes[recipe]:
                favor[ing] += self._weight_matrix[0]
        for recipe in self._recipes_made:
            for ing in recipes[recipe]:
                favor[ing] += self._weight_matrix[1]
        for recipe in self._recipes_viewed:
            for ing in recipes[recipe]:
                favor[ing] += self._weight_matrix[2]
        for ing in self._ingredients_owned.keys():
            favor[ing] += self._weight_matrix[3] * self._weight_matrix[3]
        return tanfunc(np.fromiter(favor.values(), dtype=float)).astype(int)


