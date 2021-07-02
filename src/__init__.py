
import os
from flask import Flask,jsonify
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

# define services
class Ping(Resource):
    def get(self):
        return {
        'message': 'pong!'
    }
api.add_resource(Ping, '/ping')

class GetCard(Resource):
    def get(self,recipe_id):
        #get card data dict
        card = dict()
        recipe = lookup.query('id ==' + str(recipe_id)).to_dict()
        #title,url,photo_url,rating_stars,review_count,cook_time_minutes,id
        card['title'] = recipe['title']
        card['url'] = recipe['url']
        card['photo_url'] = recipe['photo_url']
        card['rating_stars'] = recipe['rating_stars']
        card['review_count'] = recipe['review_count']
        card['cook_time_minutes'] = recipe['cook_time_minutes']
        card['id'] = recipe['id']
        return jsonify(card)
api.add_resource(GetCard, '/recipecard/<int:recipe_id>/')