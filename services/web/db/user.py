
#needs access to: current recipes database to fetch recipes
from collections import defaultdict
from pandas import DataFrame
import numpy as np
from ast import literal_eval

class User():
    def __init__(self, id, recipes_viewed, recipes_made, recipes_liked, ingredients_owned, weights):
        self._id = id
        self._recipes_viewed = recipes_viewed
        self._recipes_made = recipes_made  #if it is in made it must be in viewed
        self._recipes_liked = recipes_liked #if it is in liked it must be in viewed
        self._ingredients_owned = ingredients_owned
        self._weights = weights #like,made,view,own weights in order

    def add_like(self,id:int) -> None:
        if type(id) != int:
            raise TypeError("id type must be int- type: ",type(id))
        if id < 0:
            raise ValueError("id must be above 0- id:" ,id)
        self._recipes_liked.append(id)
    def add_view(self,id:int) -> None:
        if type(id) != int:
            raise TypeError("id type must be int- type: ",type(id))
        if id < 0:
            raise ValueError("id must be above 0- id:" ,id)
        self._recipes_viewed.append(id)
    def add_make(self,id:int) -> None:
        if type(id) != int:
            raise TypeError("id type must be int- type: ",type(id))
        if id < 0:
            raise ValueError("id must be above 0- id:" ,id)
        self._recipes_made.append(id)
    def update_ingredients(self,food:dict) -> None:
        for x,count in food.items():
            self._ingredients_owned[x] += count
    def update_weights(self,weights:list) -> None:
        if type(weights) != list:
            raise TypeError("type of weights must be list",type(weights))
        if len(weights) != 4:
            raise ValueError("list must be weight 4- len: ",len(weights))
        self._weights = weights
    def has_no_preferences(self) -> bool:
        return type(self._recipes_viewed[0]) is np.ndarray and type(self._recipes_made[0]) is np.ndarray and type(self._recipes_liked[0]) is np.ndarray and type(self._ingredients_owned[0]) is np.ndarray
    #given a list of top ingredients, return a dict that measures favorability of certain ingredients (0-1)
    #uses inverse tan function to map 0-infinity to 0-1
    #eg [corn,garlic] = [0.1,0.9]
    def get_favorability_array(self,relevant_ingredients: list,recipes:DataFrame) -> np.array:
        #relevant_ingredients: a list of ingredient (strings) to care about
        #recipes: a pandas series of lists of ingredient (strings)
        favor = dict.fromkeys(relevant_ingredients,0)
        tanfunc = lambda x: np.arctan(x/5)/ (np.pi/2)
        if len(self._weights) != 4:
            self._weights = [1,1,2,5]
        #add favor equal to weight for each recipe within input
        #modifies favor argument
        def add_favor(favor:defaultdict, input:np.ndarray, weight:int) -> None:
            if len(input) == 0:
                return
            for recipe in input:
                query = recipes.query('id == ' + str(recipe))['ingredients']
                if query.size == 0:
                    return
                if query.size > 1:
                    raise ValueError("id isn't unique")
                for ing in literal_eval(query.tolist()[0]):
                    if type(ing) == str and ing in favor:
                        favor[ing] += weight
        if self.has_no_preferences():
            add_favor(favor,[7497,115109,10312,103239,2341],self._weights[0])
        else:
            add_favor(favor,self._recipes_viewed, self._weights[0])
            add_favor(favor,self._recipes_made, self._weights[1])
            add_favor(favor,self._recipes_liked, self._weights[2])
        if len(self._ingredients_owned) > 0:
            for ing in self._ingredients_owned:
                if type(ing) is str and ing in favor:
                    print(ing)
                    favor[ing] += self._weights[3] * self._weights[3]
        return tanfunc(np.fromiter(favor.values(), dtype=float)).astype(float)


