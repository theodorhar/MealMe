import pandas as pd
import numpy as np
import json
from glob import glob

#generates a dataframe of raw data
def get_data(debug = False) -> pd.DataFrame:
    columns = ['url', 'name', 'rating', 'ingredients', 'directions', 'prep', 'cook', 'ready in', 'calories', 'ratingcount']
    raw_data = pd.DataFrame(data=[], columns=columns)
    frames = []
    for file_name in glob('*.json'):
        with open(file_name) as f:
            df = pd.read_json(f)
            frames.append(df)
    raw_data = pd.concat(frames,axis = 0, sort = True)
    raw_data.drop_duplicates(inplace = True)
    if (debug):
        print("Data read, n =",len(raw_data.index))
    return raw_data
