import pandas as pd
import numpy as np
import json
from glob import glob

#generates a dataframe of raw data
def get_raw_data(debug = False) -> pd.DataFrame:
    columns = ['url', 'name', 'rating', 'ingredients', 'directions', 'prep', 'cook', 'ready in', 'calories', 'ratingcount']
    raw_data = pd.DataFrame(data=[], columns=columns)
    frames = []
    for file_name in glob('*.json'):
        with open(file_name) as f:
            df = pd.read_json(f)
            frames.append(df)
    raw_data = pd.concat(frames,axis = 0)
    raw_data.drop_duplicates(inplace = True)
    if (debug):
        print("Data read, n =",len(raw_data.index))
    return raw_data
def get_recipe_lookup(data:pd.DataFrame,debug = False) -> pd.DataFrame:
    #['name', 'url']
    recipe_lookup = pd.DataFrame([], columns = [])
    recipe_lookup['name'] = data['name']
    recipe_lookup['url'] = data['url']
    return recipe_lookup
def get_recipes(data:pd.DataFrame,debug = False) -> pd.DataFrame:
    #['rating','region', 'ingredients', 'directions', 'prep', 'cook', 'ready in', 'calories']
    recipes = pd.DataFrame([],columns = [])
    recipes['rating'] = data['rating']
    recipes['ingredients'] = data['ingredients']
    recipes['ingredients'] = recipes['ingredients'].apply(lambda x: parse_ingredients(x))
    return recipes

def parse_ingredients(s: str) -> list:
    out = []
    return out