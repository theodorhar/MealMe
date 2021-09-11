from glob import glob
import pandas as pd
import numpy as np

def get_users(debug = False) -> pd.DataFrame:
    frames = []
    for file_name in glob('data/users.csv'):
            with open(file_name) as f:
                df = pd.read_csv(f)
                frames.append(df)
    data = pd.concat(frames,axis = 0)
    return data
def get_recipe_data(debug = False) -> pd.DataFrame:
    columns = []
    data = pd.DataFrame(data=[], columns=columns)
    frames = []
    #filename below
    for file_name in glob('data/recipes.csv'):
        with open(file_name) as f:
            df = pd.read_csv(f,dtype={'title': str, 'url': str, 'photo_url': str, 'rating_stars': np.float64,'review_count': np.int64, 'ingredients': str, 'instructions': str, 'description': str, 'author': str, 'cook_time_minutes': str, 'id': np.int64})
            frames.append(df)
    data = pd.concat(frames,axis = 0)
    data.drop_duplicates(inplace = True)
    if (debug):
        print("Data read, n =",len(data.index))
    return data

def get_recipe_lookup(debug = False) -> pd.DataFrame:
    cols = ['title','url','photo_url','rating_stars','review_count','cook_time_minutes','id']
    data = pd.DataFrame(data=[], columns = cols)
    frames = []
    #filename below
    for file_name in glob('data/recipe_lookup.csv'):
        with open(file_name) as f:
            df = pd.read_csv(f)
            frames.append(df)
    data = pd.concat(frames,axis = 0)
    if (debug):
        print("Data read, n =",len(data.index))
    return data