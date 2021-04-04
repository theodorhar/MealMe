import pandas as pd
import numpy as np
import json
import re
from glob import glob

#generates a dataframe of raw data
def get_raw_data(debug = False) -> pd.DataFrame:
    columns = ['url', 'name', 'rating', 'ingredients', 'directions', 'prep', 'cook', 'ready in', 'calories', 'ratingcount']
    raw_data = pd.DataFrame(data=[], columns=columns)
    frames = []
    for file_name in glob('*.json'):
        with open(file_name) as f:
            df = pd.read_json(f)
            frames.append(df)
    raw_data = pd.concat(frames,axis = 0)
    raw_data.drop_duplicates(inplace = True)
    raw_data.dropna(axis = 1, inplace = True, thresh = 20000)
    if (debug):
        print("Data read, n =",len(raw_data.index))
    return raw_data
def get_recipe_lookup(data:pd.DataFrame,debug = False) -> pd.DataFrame:
    #['name', 'url']
    recipe_lookup = pd.DataFrame([], columns = [])
    recipe_lookup['name'] = data['name']
    recipe_lookup['url'] = data['url']
    return recipe_lookup
def get_recipes(data:pd.DataFrame,debug = False) -> pd.DataFrame:
    recipes = pd.DataFrame([],columns = [])
    recipes['rating'] = data['rating']
    recipes['ingredients'] = data['ingredients']
    recipes['ingredients'] = recipes['ingredients'].apply(parse_ingredients)
    recipes['ingredient_len'] = recipes['ingredients'].apply(lambda x: len(x))
    recipes['directions_len'] = data['directions'].apply(lambda x: len(re.split(r'[0-9]\.',x)))
    recipes['directions_sent_len'] = data['directions'].apply(lambda x: len(x.split('.')))
    recipes['directions_char_len'] = data['directions'].apply(lambda x: len(x))
    recipes['prep'] = data['prep'].apply(parse_time)
    recipes['cook'] = data['cook'].apply(parse_time)
    recipes['ready'] = data['ready in'].apply(parse_time)
    recipes['calories'] = data['calories']
    if debug:
        print("Recipe data loaded")
    return recipes
#standardize ingredients
def parse_ingredients(input_str: str) -> list:
    splitstr = input_str.split(', ')
    out = []
    words = (r'large|medium|small|and|cut|into|sheet(s)?|frozen| in |half|crosswise | raw'
    r'|lengthwise|pinch|whole|short|long| of |torn|strip(s)?|halves|inch(es)?|centimeter(s)?|'
    r'ground| thin(ly)?| thick(ly)?|pieces|cup(s)?|teaspoon(s)?|tablespoon(s)?| can | cube(s)?|pounds|pound'
    r'for|frying|end(s)?|dash(es)?|ounce(s)?|clove(s)?|bunch(es)?|(?<!\w)or(?!\w)|(?<!\w)to(?!\w)|taste|fresh(ly)?'
    r'such|for |coarse(ly)?|(non)?fat |stems|more|(?<!\w)as(?!\w)|fatfree|lightly|beaten'
    r'extravirgin|slice(s)?|round|diameter|package(s)?|without|shells| room| temperature|garnish'
    r'slice(s)?|jar|loaf|container|the liquid|fine(ly)?|across bones|drop(s)|can(s)? |(?<= )d(?!\w)|(?<!\w)d(?= )'
    r'grain|sprig(s)?|(?<!pork )ear(s)? |(low)?sodium|head |ium |boiling |(?<!\w)log(?!\w)'
    r'leaf|leaves|envelope|roma |quart(s)|bottle|cold| hot |link ')
    for item in splitstr:
        s = item
        #remove parens
        s = re.sub(r'\(.*\)','',s.strip())
        #remove symbols
        s = re.sub(r'([0-9])*([^\w\s])*',"",s.strip())
        s = re.sub(r'[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞↉]+', "", s.strip())
        #remove words
        s = re.sub(r'(\w)+(?<! se| ch)(ed)(?!d)', '',s.strip())
        s = re.sub(words, '',s.strip())
        #round 2
        s = re.sub(r'pound(s)?|fresh|ly  |thin(ly)?|(?<!\w)s ','',s.strip())
        
        #done with regex
        if s.strip() != "":
            out.append(s.strip())
    return out
#parse a time using "hr" and "mins" formatting
def parse_time(input_str: str) -> int:
    out = 0
    if len(input_str) < 5 and not bool(re.match(r'[0-9]* hr',input_str.strip())):
        return None
    if bool(re.match(r'[0-9]* hr(s)? [0-9]* mins',input_str.strip())):
        out += 60 * int(input_str[0])
        if len(input_str.split(' ')) > 2:
            out += int(input_str.split(' ')[2])
    elif bool(re.match(r'[0-9]* hr',input_str.strip())):
        out += 60 * int(input_str[0])
    elif bool(re.match(r'[0-9]* mins',input_str.strip())):
        out = int(input_str.split(" ")[0])
    else:
        return None
    return out