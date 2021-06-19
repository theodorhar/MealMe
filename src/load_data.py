import pandas as pd
from glob import glob

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
    print(data)
    if (debug):
        print("Data read, n =",len(data.index))
    return data

def get_recipe_lookup(debug = False) -> pd.DataFrame:
    columns = ['name','url']
    data = pd.DataFrame(data=[], columns=columns)
    frames = []
    #filename below
    for file_name in glob('data/lookup.csv'):
        with open(file_name) as f:
            df = pd.read_csv(f)
            frames.append(df)
    data = pd.concat(frames,axis = 0)
    data.drop_duplicates(inplace = True)
    data.dropna(axis = 1, inplace = True)
    print(data)
    if (debug):
        print("Data read, n =",len(data.index))
    return data