
import os, random, requests, json
from flask import Flask,jsonify,Response,request,url_for,redirect,g
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_restx import Api,Resource
from mysql.connector import pooling
from oauthlib.oauth2 import WebApplicationClient

from pandas.core.frame import DataFrame
from rapidfuzz import fuzz
from rapidfuzz import process

# Internal imports
from db.user import User
from api.load_data import get_recipe_lookup

# Configuration
DEBUG = False
google_client_id_file = open('/run/secrets/google-client-id', 'r')
GOOGLE_CLIENT_ID = google_client_id_file.read()
google_client_id_file.close()
google_client_secret_file = open('/run/secrets/google-client-secret', 'r')
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
google_client_secret_file.close()
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# instantiate the app
app = Flask(__name__)
api = Api(app)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)  

#load entire dataset into memory
lookup = get_recipe_lookup(debug = DEBUG)
#MySQL connection pool initialization
pf = open('/run/secrets/db-users-password', 'r')
userdbconfig = {
"database": "panoplydb",
"user":     "admin_users",
"host":     "db",
"password": pf.read()
}
userpool = pooling.MySQLConnectionPool(pool_name = "userpool", pool_size = 20, **userdbconfig)
pf.close()

#login session handler
login_manager = LoginManager()
login_manager.init_app(app)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

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

class Home(Resource):
    def get(self):
        if current_user.is_authenticated:
            return (
                "<p>Hello, {}! You're logged in! Email: {}</p>"
                "<div><p>Google Profile Picture:</p>"
                '<img src="{}" alt="Google profile pic"></img></div>'
                '<a class="button" href="/logout">Logout</a>'.format(
                    current_user.name, current_user.email, current_user.profile_pic
                )
            )
        else:
            return '<a class="button" href="/login">Google Login</a>'
api.add_resource(Home, "/index")

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

class Login(Resource):
    def get(self):
        # Find out what URL to hit for Google login
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)
api.add_resource(Login ,"/login")

class Login_Callback(Resource):
    def get(self):
        # Get authorization code Google sent back to you
        code = request.args.get("code")
        # Find out what URL to hit to get tokens that allow you to ask for
        # things on behalf of a user
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        # Prepare and send a request to get tokens! Yay tokens!
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )

        # Parse the tokens!
        client.parse_request_body_response(json.dumps(token_response.json()))
        # Now that you have tokens (yay) let's find and hit the URL
        # from Google that gives you the user's profile information,
        # including their Google profile image and email
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        # You want to make sure their email is verified.
        # The user authenticated with Google, authorized your
        # app, and now you've verified their email through Google!
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
        else:
            return "User email not available or not verified by Google.", 400
        # Create a user in your db with the information provided
        # by Google
        user = User(
            id_=unique_id, name=users_name, email=users_email, profile_pic=picture
        )

        # Doesn't exist? Add it to the database.
        if not User.get(unique_id):
            User.create(unique_id, users_name, users_email, picture)

        # Begin user session by logging the user in
        login_user(user)

        # Send user back to homepage
        return redirect(url_for("index"))

api.add_resource(Login_Callback, "/login/callback")


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