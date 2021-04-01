import pandas as pd
import numpy as np
import tensorflow as tf
import data_processing
import collections
DEBUG = True

#takes in dataset and user embedding, outputs recommendations
data = data_processing.get_data(debug = DEBUG)

feature_columns = []
ratings_numeric = tf.feature_column.numeric_column("rating")
ratings_buckets = pd.qcut(data['rating'], q=10, retbins=True)
ratings = tf.feature_column.bucketized_column(ratings_numeric,list(ratings_buckets[1]))
feature_columns.append(ratings)
