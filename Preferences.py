import numpy as np
import tensorflow as tf
import pandas as pd
#storage of user preferences
class Preferences(object):
    _regions = ['Spain', 'Thailand', 'Misc.: Portugal', 'Japan', 'British Isles', 'China', 'France', 
        'DACH Countries', 'South East Asia', 'Middle East', 'Canada', 'Italy', 'Mexico', 'Misc.: Dutch',
        'Misc.: Central America', 'South America', 'Greece', 'USA', 'Eastern Europe', 'Australia & NZ', 
        'Indian Subcontinent', 'Africa', 'Scandinavia', 'Caribbean', 'Korea', 'Misc.: Belgian']
    _cols = ["userid","region","ingredients","isVegeterian","isVegan","allergies","skill", "effort"]
    _ingredientlist = [""]
    def __init__(self):
        self._dataFrame = pd.DataFrame(data = [], columns = self._cols)
    