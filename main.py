import json
import time
from pathlib import Path
from wsgiref.util import request_uri

from flask import Flask
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_mail import Mail, Message
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

from api.v1_0.campaigns import (
    campaigns_api,
    db_campaigns,
    get_campaigns,
    toggle_player_web,
)
from api.v1_0.message_keys import message_keys
from api.v1_0.models import User
from app_configurator import configure
from db import Database, make_file
from db import dbsql as db

from handle_apikeys import generate, put

app = Flask(__name__)
# Register the blueprint in api/v1_0/campaigns.py

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "nerdsplaypnpvalidator@gmail.com"
app.config["MAIL_PASSWORD"] = "xwebtezpptgxfcbs"  #'$52ceP^1xbMU'
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config[
    "SECRET_KEY"
] = "e6405ba489b12b5c3e736e70094c315c85132c5cb16bd2c5cfbbbe47868bfe32"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
mail = Mail(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
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
    # Register all the blueprints
    # We have to do this here to avoid circle import
    from api.v1_0.auth import auth
    from api.v1_0.campaigns import campaigns_api
    from api.v1_0.email import email
    from api.v1_0.website_logic import weblogic

    app.register_blueprint(email)
    app.register_blueprint(campaigns_api)
    app.register_blueprint(weblogic)
    app.register_blueprint(auth)

    # uncomment the following line to create the user database on startup
    db.create_all(app=app)
    app.run(port=7777, debug=True)
