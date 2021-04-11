from . import data_processing, user

import collections as col
import pandas as pd
import tensorflow as tf
import numpy as np
from numpy.linalg import norm
import heapq



DEBUG = True
def n_most_freq(ser:pd.Series,n:int) -> list:
    d = col.defaultdict(lambda:0)
    for x in ser:
        for item in x:
            d[item] += 1
    return [x[0] for x in sorted(d.items(),key = lambda x:x[1])[-n:][::-1]]
#print(n_most_freq(recipes['ingredients'],50))
def cosine_similarity(u:user, rec:np.array):
    if norm(u) == 0:
        raise ValueError('User has preference norm 0, invalid')
    if norm(rec) == 0:
        return 0
    return np.dot(u, rec)/(norm(u)*norm(rec))

#linearly calculates all distances from the user to the recipes
def get_recommendations(u:user, df:pd.DataFrame, n:int) -> np.array:
    ratings = []
    relevant_ingredients = n_most_freq(df['ingredients'],50)
    for r in df.iloc()[0:1000].iloc():
        one_hot_ingredients = []
        for x in relevant_ingredients:
            one_hot_ingredients.append(1 if x in r['ingredients'] else 0)
        if r['id'] % 50 == 0:
            print(r['id'],"searched, ", len(df['id']) - r['id'],"to go.")
        ratings.append( (r['id'],cosine_similarity(u.get_favorability_array(relevant_ingredients,df),one_hot_ingredients)) ) #tuple
    return heapq.nlargest(n,ratings,key = lambda x:x[1])
