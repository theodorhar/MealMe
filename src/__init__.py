
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
    
@api.route('/<int:recipe_id>')
class GetCard(Resource):
    def get(self,recipe_id):
        #get card data dict
        card = {}
        recipe = lookup.query('id ==' + str(recipe_id))
        card['id'] = recipe['id']
        card['name'] = recipe['name']
        card['url'] = recipe['url']
        return jsonify(card)
api.add_resource(Ping, '/ping')
api.add_resource(GetCard, '/recipecard')