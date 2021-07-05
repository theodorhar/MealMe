
import os, random
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
#construct favored
querystr = 'id < 62343 and review_count > 3000 or id > 80859 and review_count > 500'
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
        #get card data dict
        card = dict()
        recipe = lookup.query('id ==' + str(recipe_id)).to_dict()
        #title,url,photo_url,rating_stars,review_count,cook_time_minutes,id
        card['title'] = recipe['title'][recipe_id]
        card['url'] = recipe['url'][recipe_id]
        card['photo_url'] = recipe['photo_url'][recipe_id]
        card['rating_stars'] = recipe['rating_stars'][recipe_id]
        card['review_count'] = recipe['review_count'][recipe_id]
        card['cook_time_minutes'] = recipe['cook_time_minutes'][recipe_id]
        card['id'] = recipe['id'][recipe_id]
        return jsonify(card)
api.add_resource(GetCard, '/recipecard/<int:recipe_id>/')

class default(Resource):
    def get(self):
        if len(favored) > 10:
            indices = []
            alreadyDisplayed = []
            for _ in range(10):
                index = random.randint(0,len(favored)-1)
                while(index in alreadyDisplayed):
                    index = random.randint(0,len(favored)-1)
                indices.append(index)
                
            return jsonify(favored.iloc[indices].to_dict())
        else:
            return jsonify(favored.to_dict())
api.add_resource(default, '/default')