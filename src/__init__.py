
import os, random
from flask import Flask,jsonify,Response
from flask_restx import Api,Resource
from src.load_data import get_recipe_lookup
DEBUG = False

# instantiate the app
app = Flask(__name__)
api = Api(app)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)  

#load entire dataset into memory
lookup = get_recipe_lookup(debug = DEBUG)
#construct favored
querystr = 'id < 62343 and review_count > 3000 or id > 80859 and review_count > 400'
favored = lookup.query(querystr)
# define services
class Ping(Resource):
    def get(self):
        return {
        'message': 'pong!'
    }
api.add_resource(Ping, '/ping')

class GetCard(Resource):
    def get(self,recipe_id):
        #title,url,photo_url,rating_stars,review_count,cook_time_minutes,id
        return Response(lookup.query('id ==' + str(recipe_id)).to_json(orient="records"), mimetype='application/json')
api.add_resource(GetCard, '/recipecard/<int:recipe_id>/')

class Default(Resource):
    def get(self):
        NUMRESULTS = 20
        if len(favored) > NUMRESULTS:
            indices = list(range(len(favored)))
            random.shuffle(indices)
            indices = indices[:NUMRESULTS]
            return Response(favored.iloc[indices].to_json(orient="records"), mimetype='application/json')
        else:
            return jsonify(favored.to_dict())
api.add_resource(Default, '/default')