from glob import glob
import pandas as pd

def get_recipe_data(debug = False) -> pd.DataFrame:
    columns = ['rating','ingredients','ingredient_len','directions_len','directions_sent_len','directions_char_len','prep','cook','ready','calories','id']
    data = pd.DataFrame(data=[], columns=columns)
    frames = []
    #filename below
    for file_name in glob('data/recipes.csv'):
        with open(file_name) as f:
            df = pd.read_csv(f)
            frames.append(df)
    data = pd.concat(frames,axis = 0)
    data.drop_duplicates(inplace = True)
    data.dropna(axis = 1, inplace = True)
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