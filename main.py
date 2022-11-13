import json, uuid
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

from api.v1_0.message_keys import message_keys
from app_configurator import configure
from api.v2_0.models import dbsql as db
from handle_apikeys import generate, put
from api.v2_0.models import User
from api.v2_0.authentication import *


app = Flask(
    __name__, template_folder=Path("page/templates"), static_folder=Path("page/static")
)
# Register the blueprint in api/v1_0/campaigns.py
app = configure(app)  # Done to hide
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/db/db.sqlite"
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
    db.create_all(app=app)
    put(generate())
    # Register all the blueprints
    # We have to do this here to avoid circle import
    from api.v1_0.campaigns import campaigns_api_v1
    from api.v2_0.campaigns import campaigns_api_v2
    from api.v2_0.authentication import authentication
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
    app.register_blueprint(campaigns_api_v1)
    app.register_blueprint(auth)
    app.register_blueprint(authentication)
    app.register_blueprint(admin_page)
    app.register_blueprint(campaigns)
    app.register_blueprint(dm_page)
    app.register_blueprint(imprint)
    app.register_blueprint(index_page)
    app.register_blueprint(mentor)
    app.register_blueprint(profile)
    app.register_blueprint(message_keys)
    app.register_blueprint(campaigns_api_v2)

    # uncomment the following line to create the user database on startup
    app.run(port=7777, debug=True)
