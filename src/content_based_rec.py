import io
import os
import re
import shutil
import collections as col
import string
import pandas as pd
import tensorflow as tf
import numpy as np
from numpy.linalg import norm
import data_processing
import user

from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

DEBUG = True

raw_data = data_processing.get_raw_data(debug = DEBUG)
recipes = data_processing.get_recipes(raw_data, debug = DEBUG)
print(recipes)
# counts = col.defaultdict(lambda: 0)
# def n_most_freq(ser:pd.Series,n:int) -> list:
#     d = col.defaultdict(lambda:0)
#     for x in ser:
#         for item in x:
#             d[item] += 1
#     return sorted(d.items(),key = lambda x:x[1])[-n:][::-1]
# #print(n_most_freq(recipes['ingredients'],50))
# def cosine_similarity(u:user, rec:np.array):
#     if norm(u) == 0:
#         raise ValueError('User has preference norm 0, invalid')
#     if norm(rec) == 0:
#         return 0
#     return np.dot(u, rec)/(norm(u)*norm(rec))
# def get_recommendations(u:user, df:pd.DataFrame, n:int) -> np.array:
#     out = np.array([])
    
#     return out