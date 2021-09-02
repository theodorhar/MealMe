
import collections as col
import pandas as pd
import numpy as np
from numpy.linalg import norm
import heapq
from ast import literal_eval


DEBUG = True
def n_most_freq(ser:pd.Series,n:int) -> list:
    d = col.defaultdict(lambda:0)
    for x in ser:
        if type(x) is str:
            for item in literal_eval(x):
                d[item] += 1
        else:
            raise TypeError("invalid format, series doesn't contain strings")
    return [x[0] for x in sorted(d.items(),key = lambda x:x[1])[-n:][::-1]]
#print(n_most_freq(recipes['ingredients'],50))
def cosine_similarity(u, rec:np.array):
    if norm(u) == 0:
        raise ValueError('User has preference norm 0, invalid')
    if norm(rec) == 0:
        return 0
    return np.dot(u, rec)/(norm(u)*norm(rec))

#linearly calculates all distances from the user to the recipes
def get_recommendations(u, df:pd.DataFrame, n:int) -> np.array:
    ratings = []
    relevant_ingredients = n_most_freq(df['ingredients'],50)
    ing_favor = u.get_favorability_array(relevant_ingredients,df)
    for r in df.iloc():
        one_hot_ingredients = []
        for x in relevant_ingredients:
            one_hot_ingredients.append(1 if x in r['ingredients'] else 0)
        ratings.append( (r['id'],cosine_similarity(ing_favor,one_hot_ingredients)) ) #tuple
    return heapq.nlargest(n,ratings,key = lambda x:x[1])
