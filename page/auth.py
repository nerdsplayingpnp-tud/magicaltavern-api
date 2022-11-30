from main import discord, app
from flask import request, abort, Blueprint
from api.v2_0.models import dbsql as db
from api.v2_0.models import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return discord.create_session()
