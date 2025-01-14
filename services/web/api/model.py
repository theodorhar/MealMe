from web import load_data
import pandas as pd
import numpy as np
import tensorflow as tf
import collections
from load_data import get_recipe_data,get_recipe_lookup
#takes in dataset and user embedding, outputs recommendations
DEBUG = True


recipes = get_recipe_data()
print(recipes)
recipe_lookup = get_recipe_lookup()

feature_columns = []
#feature column definition
#adds a cross of two (bucketed) columns from a dataframe to the feature_columns list
def add_cross(data:pd.DataFrame, feature_columns:list, cols:list, num_buckets:list, hash_bucket_size = 100) -> None:
    if len(cols) != len(num_buckets):
        raise ValueError("len of cols(" + str(len(cols)) + ") must equal len of num_buckets("+ str(len(num_buckets))+").")
    fcols = []
    for col,bnum in zip(cols,num_buckets):
        numeric_col = tf.feature_column.numeric_column(col)
        buckets_one = pd.qcut(data[col], q=bnum, retbins=True) 
        feature_col = tf.feature_column.bucketized_column(numeric_col,list(buckets_one[1]))
        fcols.append(feature_col)
    cross = tf.feature_column.crossed_column(fcols,hash_bucket_size=hash_bucket_size) 
    crossed_features = tf.feature_column.indicator_column(cross)

    feature_columns.append(crossed_features)

def add_bucketed_col(data:pd.DataFrame, feature_columns:list, col:str,num_buckets = 10) -> None:
    numeric_col = tf.feature_column.numeric_column(col)
    buckets = pd.qcut(data[col], q=num_buckets, retbins=True) 
    feature_col= tf.feature_column.bucketized_column(numeric_col,list(buckets[1]))
    feature_columns.append(feature_col)

add_bucketed_col(recipes,feature_columns,"rating",10)
add_cross(recipes, feature_columns, ["directions_sent_len", "directions_char_len"], [10,10], 100)
#add_cross(recipes,feature_columns,"prep","cook",7,7,100)
