from wsgiref.util import request_uri
from werkzeug.security import generate_password_hash, check_password_hash
from flask import *
from flask_login import LoginManager, current_user,login_user, login_required, logout_user
from flask_mail import Mail, Message
from handle_apikeys import generate, put
from pathlib import Path
from api.v1_0.campaigns import campaigns_api
from api.v1_0.message_keys import message_keys
from db import Database, make_file, dbsql as db
import json, time
from api.v1_0.campaigns import get_campaigns, db_campaigns, toggle_player_web
from api.v1_0.models import User

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

app = Flask(__name__)
# Register the blueprint in api/v1_0/campaigns.py
app.register_blueprint(campaigns_api)
app.register_blueprint(message_keys)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nerdsplaypnpvalidator@gmail.com'
app.config['MAIL_PASSWORD'] = 'xwebtezpptgxfcbs' #'$52ceP^1xbMU'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KEY'] = 'e6405ba489b12b5c3e736e70094c315c85132c5cb16bd2c5cfbbbe47868bfe32'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
mail = Mail(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
# Register a route
@app.route("/api/v1.0/", methods=["GET"])
def home_page():
    return json.dumps("API is online.")

@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

if __name__ == "__main__":
    put(generate())
    #Register all the blueprints
    #We have to do this here to avoid circle import
    from api.v1_0.auth import auth
    from api.v1_0.website_logic import weblogic
    from api.v1_0.campaigns import campaigns_api
    from api.v1_0.email import email
    app.register_blueprint(email)
    app.register_blueprint(campaigns_api)
    app.register_blueprint(weblogic)
    app.register_blueprint(auth)

    #uncomment the following line to create the user database on startup
    db.create_all(app=app)
    app.run(port=7777, debug=True)
