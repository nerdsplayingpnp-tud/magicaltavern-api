import json
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
from app_configurator import configure
from db import Database
from db import dbsql as db
from db import make_file
from handle_apikeys import generate, put
from page.models import User
from page.routes.admin_page import AdminPage
from page.routes.campaigns import campaign_page
from page.routes.dm_page import DmPage
from page.routes.imprint import impressum_page

app = Flask(
    __name__, template_folder=Path("page/templates"), static_folder=Path("page/static")
)
# Register the blueprint in api/v1_0/campaigns.py
app = configure(app)
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
    from api.v1_0.campaigns import campaigns_api
    from page.auth import auth
    from page.email import email
    from page.routes.admin_page import admin_page
    from page.routes.campaigns import campaigns
    from page.routes.dm_page import dm_page
    from page.routes.imprint import imprint
    from page.routes.index import index as index_page
    from page.routes.mentor import mentor
    from page.routes.profile import profile

    app.register_blueprint(email)
    app.register_blueprint(campaigns_api)
    app.register_blueprint(auth)
    app.register_blueprint(admin_page)
    app.register_blueprint(campaigns)
    app.register_blueprint(dm_page)
    app.register_blueprint(imprint)
    app.register_blueprint(index_page)
    app.register_blueprint(mentor)
    app.register_blueprint(profile)

    # uncomment the following line to create the user database on startup
    db.create_all(app=app)
    app.run(port=7777, debug=True)
