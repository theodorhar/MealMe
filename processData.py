import pandas as pd
import numpy as np
import json
from glob import glob

columns = ['url', 'name', 'rating', 'ingredients', 'directions', 'prep', 'cook', 'ready in', 'calories', 'ratingcount']
dataFrame = pd.DataFrame(data=[], columns=columns)
frames = []
for file_name in glob('*.json'):
    with open(file_name) as f:
        df = pd.read_json(f)
        frames.append(df)
dataFrame = pd.concat(frames,axis = 0, sort = True)
dataFrame.drop_duplicates(inplace = True)

#now we have a dataframe of raw data