import io
import os
import re
import shutil
import collections as col
import string
import pandas as pd
import tensorflow as tf
import data_processing

from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

DEBUG = True

raw_data = data_processing.get_raw_data(debug = DEBUG)
recipes = data_processing.get_recipes(raw_data, debug = DEBUG)
counts = col.defaultdict(lambda: 0)
def n_most_freq(ser:pd.Series,n:int) -> list:
    d = col.defaultdict(lambda:0)
    for x in ser:
        for item in x:
            d[item] += 1
    return sorted(d.items(),key = lambda x:x[1])[-n:][::-1]
print(n_most_freq(recipes['ingredients'],50))
embedding_layer = tf.keras.layers.Embedding(1000, 10)
