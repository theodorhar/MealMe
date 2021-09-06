from ast import literal_eval
import pandas as pd
import re
from glob import glob

#generates a dataframe of raw data from jsons within the data folder
def get_raw_data(debug = False) -> pd.DataFrame:
    #columns = ['url', 'name', 'rating', 'ingredients', 'directions', 'prep', 'cook', 'ready in', 'calories', 'ratingcount'] #the original format
    #allrecipes
    #columns = ["author","prep_time_minutes","description","footnotes", "ingredients","photo_url","cook_time_minutes","rating_stars","review_count","time_scraped","title","total_time_minutes","url"]
    #epicurious
    columns = ["id","dek","hed","author","type","url","photoData","tag","aggregateRating","ingredients","prepSteps","reviewsCount","willMakeAgainPct","dateCrawled"]
    #bbccouk
    #columns = ['chef', 'chef_id', 'cooking_time_minutes', 'description', 'ingredients', 'instructions', 'photo_url', 'preparation_time_minutes', 'title', 'total_time_minutes', 'url']
    #cookstr
    #columns = ["chef","description", "dietary_considerations", "ingredients", 'instructions', 'photo_url',"rating_count","rating_value",'title', 'url']
    raw_data = pd.DataFrame(data=[], columns=columns)
    frames = []
    for file_name in glob('data/epicurious-recipes.json'): #change this to file name of data source
        with open(file_name) as f:
            df = pd.read_json(f, lines = True)
            frames.append(df)
    raw_data = pd.concat(frames,axis = 0)
    # raw_data = raw_data[raw_data.cook_time_minutes != 0]
    #raw_data = raw_data[raw_data.review_count != 0]
    #raw_data.drop_duplicates(inplace = True)
    #raw_data.dropna(axis = 1, inplace = True)
    if (debug):
        print("Data read, n =",len(raw_data.index))
    return raw_data
#data needed for a card
def write_recipe_lookup_allrecipes(data:pd.DataFrame,path: str,debug = False) -> pd.DataFrame:
    recipe_lookup = pd.DataFrame([], columns = [])
    recipe_lookup['title'] = data['title']
    recipe_lookup['url'] = data['url']
    recipe_lookup['photo_url'] = data['photo_url']
    recipe_lookup['rating_stars'] = data['rating_stars']
    recipe_lookup['review_count'] = data['review_count']
    recipe_lookup['cook_time_minutes'] = data['cook_time_minutes']
    if (debug):
        print(recipe_lookup)
    recipe_lookup.to_csv(path,index = False)
def write_recipe_lookup_bbccouk(data:pd.DataFrame,path: str,debug = False) -> pd.DataFrame:
    recipe_lookup = pd.DataFrame([], columns = [])
    recipe_lookup['title'] = data['title']
    recipe_lookup['url'] = data['url']
    recipe_lookup['photo_url'] = data['photo_url']
    recipe_lookup['rating_stars'] = None
    recipe_lookup['review_count'] = 0
    recipe_lookup['cook_time_minutes'] = data['cooking_time_minutes']
    if (debug):
        print(recipe_lookup)
    recipe_lookup.to_csv(path,index = False)
def write_recipe_lookup_cookstr(data:pd.DataFrame,path: str,debug = False) -> pd.DataFrame:
    recipe_lookup = pd.DataFrame([], columns = [])
    recipe_lookup['title'] = data['title']
    recipe_lookup['url'] = data['url']
    recipe_lookup['photo_url'] = data['photo_url']
    recipe_lookup['rating_stars'] = data['rating_value']
    recipe_lookup['review_count'] = data['rating_count']
    recipe_lookup['cook_time_minutes'] = data['total_time']
    if (debug):
        print(recipe_lookup)
    recipe_lookup.to_csv(path,index = False)
def write_recipe_lookup_epic(data:pd.DataFrame,path: str,debug = False) -> pd.DataFrame:
    recipe_lookup = pd.DataFrame([], columns = [])
    recipe_lookup['title'] = data['hed']
    recipe_lookup['url'] = "epicurious.com"+data['url']
    photo_ids = [x['id'] for x in data['photoData'].to_dict().values()]
    recipe_lookup['photo_url'] = photo_ids
    recipe_lookup['photo_url']="https://assets.epicurious.com/photos/"+recipe_lookup['photo_url']+"/"
    recipe_lookup['rating_stars'] = data['aggregateRating'] / 4 * 5
    recipe_lookup['review_count'] = data['reviewsCount']
    recipe_lookup['cook_time_minutes'] = 0
    if (debug):
        print(recipe_lookup)
    recipe_lookup.to_csv(path,index = False)
def write_recipes_allrecipes(data:pd.DataFrame,path: str,debug = False) -> pd.DataFrame:
    recipes = pd.DataFrame([], columns = [])
    recipes['title'] = data['title']
    recipes['url'] = data['url']
    recipes['photo_url'] = data['photo_url']
    recipes['rating_stars'] = data['rating_stars']
    recipes['review_count'] = data['review_count']
    recipes['ingredients'] = data['ingredients']
    recipes['instructions'] = data['instructions']
    recipes['description'] = data['description']
    recipes['author'] = data['author']
    recipes['cook_time_minutes'] = data['cook_time_minutes']
    if (debug):
        print(recipes)
    recipes.to_csv(path,index = False)
def write_recipes_bbccouk(data:pd.DataFrame,path: str,debug = False) -> pd.DataFrame:
    recipes = pd.DataFrame([], columns = [])
    recipes['title'] = data['title']
    recipes['url'] = data['url']
    recipes['photo_url'] = data['photo_url']
    recipes['rating_stars'] = None
    recipes['review_count'] = 0
    recipes['ingredients'] = data['ingredients']
    recipes['instructions'] = data['instructions']
    recipes['description'] = data['description']
    recipes['author'] = data['chef']
    recipes['cook_time_minutes'] = data['cooking_time_minutes']
    if (debug):
        print(recipes)
    recipes.to_csv(path,index = False)
def write_recipes_cookstr(data:pd.DataFrame,path: str,debug = False) -> pd.DataFrame:
    recipes = pd.DataFrame([], columns = [])
    recipes['title'] = data['title']
    recipes['url'] = data['url']
    recipes['photo_url'] = data['photo_url']
    recipes['rating_stars'] = data['rating_value']
    recipes['review_count'] = data['rating_count']
    recipes['ingredients'] = data['ingredients']
    recipes['instructions'] = data['instructions']
    recipes['description'] = data['description']
    recipes['author'] = data['chef']
    recipes['cook_time_minutes'] = data['total_time']
    if (debug):
        print(recipes)
    recipes.to_csv(path,index = False)

def write_recipes_epic(data:pd.DataFrame,path: str,debug = False) -> pd.DataFrame:
    recipes = pd.DataFrame([], columns = [])
    recipes['title'] = data['hed']
    recipes['url'] = "epicurious.com"+data['url']
    photo_ids = [x['id'] for x in data['photoData'].to_dict().values()]
    recipes['photo_url'] = photo_ids
    recipes['photo_url']="https://assets.epicurious.com/photos/"+recipes['photo_url']+"/"
    recipes['rating_stars'] = data['aggregateRating'] / 4 * 5
    recipes['review_count'] = data['reviewsCount']
    recipes['ingredients'] = data['ingredients']
    recipes['instructions'] = data['prepSteps']
    recipes['description'] = data['dek']
    recipes['author'] = [x for x in data['author']]
    recipes['cook_time_minutes'] = 0
    if (debug):
        print(recipes)
    recipes.to_csv(path,index = False)

# recipes = get_raw_data(debug = True)
# path = "data/more/recipes_epic.csv"
# write_recipes_epic(recipes, path, debug=True)
def add_index(path:str, debug = False)->None:
    columns = ['title','url','photo_url','rating_stars','review_count','cook_time_minutes','id']
    data = pd.DataFrame(data=[], columns=columns)
    frames = []
    for file_name in glob(path):
        with open(file_name) as f:
            df = pd.read_csv(f)
            frames.append(df)
    data = pd.concat(frames,axis = 0)
    data['id'] = range(0,len(data))
    data.to_csv(path,index = False)
add_index(path = 'data/recipes.csv')
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
    recipes['id'] = range(0,len(recipes))
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