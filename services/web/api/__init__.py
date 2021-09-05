
import os, random
from flask import Flask, jsonify,Response,request
from flask_restx import Api,Resource

from numpy import empty, zeros
from pandas.core.frame import DataFrame
from pandas.io.parquet import read_parquet
from rapidfuzz import fuzz
from rapidfuzz import process

# Internal imports
from db.user import User
from api.load_data import get_recipe_lookup, get_users, get_recipe_data
from api.content_based_rec import get_recommendations
# configuration
DEBUG = False

# instantiate the app
app = Flask(__name__)
api = Api(app)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)  
app.secret_key = os.urandom(24)

#re-initialize(to empty) dataframes within docker volume
RESET_VOLUME = True
if RESET_VOLUME:
    lookup = get_recipe_lookup(debug = DEBUG)
    users = get_users(debug = DEBUG)
    recipes = get_recipe_data(debug = DEBUG)
    #save to volume
    recipes.to_parquet("/app/recipes.parquet")
    users.to_parquet("/app/users.parquet")
    lookup.to_parquet("/app/lookup.parquet")

# load dataframes
lookup = read_parquet("/app/lookup.parquet")

#data preprocessing
#construct favored
querystr = 'id < 71906 and review_count > 3000 or id > 90422 and review_count > 400'
favored = lookup.query(querystr)

# define API services

class Ping(Resource):
    def get(self):
        return {
        'message': 'pong!'
    }
api.add_resource(Ping, '/ping')

class Card(Resource):
    def get(self,recipe_id):
        #title,url,photo_url,rating_stars,review_count,cook_time_minutes,id
        return Response(lookup.query('id ==' + str(recipe_id)).to_json(orient="records"), mimetype='application/json')
    def post(self,title,url,photo_url,rating_stars,review_count,cook_time_minutes,id):
        pass
        #create recipe entry
        #save data to buffer file

api.add_resource(Card, '/recipecard/<int:recipe_id>/')

class Default(Resource):
    def get(self):
        NUMRESULTS = 30
        if len(favored) > NUMRESULTS:
            indices = list(range(len(favored)))
            random.shuffle(indices)
            indices = indices[:NUMRESULTS]
            return Response(favored.iloc[indices].to_json(orient="records"), mimetype='application/json')
        else:
            return jsonify(favored.to_dict())
api.add_resource(Default, '/default')

class Search(Resource):
    def get(self):
        NUMRESULTS = 30
        THRESHOLD = 80
        query = request.args.get('q')
        choices = lookup.loc[:,'title'].tolist()
        res = process.extract(query,choices,limit = NUMRESULTS,scorer=fuzz.partial_ratio)
        #[(title:str,percent match:double,id:int):tuple]:list

        #collect required information about card and output
        out = DataFrame()
        for _,percent_match,id in res:
            if percent_match > THRESHOLD:
                card = lookup.query('id ==' + str(id)).copy()
                card.loc[:,'percent_match'] = percent_match
                out = out.append(card)
        return Response(out.to_json(orient="records"), mimetype='application/json')
api.add_resource(Search, '/search')
class Recommend(Resource):
    def get(self): #assumes: id doesn't change for user
        id = str(request.headers.get('Authorization'))
        users = read_parquet("/app/users.parquet")
        if id not in users.id.values:
            newuser = {"id":id,"recipes_viewed":empty(0),"recipes_made":empty(0),"recipes_liked":empty(0),"ingredients_owned":empty(0),"weights":empty(0)}
            #add user to data
            users = users.append(newuser, ignore_index = True)
            users.to_parquet("/app/users.parquet")
        #return Response(users.to_json(orient="records"), mimetype='application/json')
        
        #recommend something
        u = users.query("id == @id")
        
        user = User(id, u["recipes_viewed"].to_list(), u["recipes_made"].to_list(), u["recipes_liked"].to_list(), u["ingredients_owned"].to_list(),u["weights"].to_list())
        recipes = read_parquet("/app/recipes.parquet")
        results = get_recommendations(user, recipes, 30)
        formatted_results = [{**lookup.query("id == @i").to_dict('records')[0],'confidence':float(confidence)} for i,confidence in results]
        return jsonify(formatted_results)
api.add_resource(Recommend, '/recommend')