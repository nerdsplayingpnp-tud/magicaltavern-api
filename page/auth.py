from main import discord, app
from flask import request, abort, Blueprint, redirect
from api.v2_0.models import dbsql as db
from api.v2_0.models import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return discord.create_session()


@auth.route("/callback")
def callback():
    data = discord.callback()
    redirect_to = data.get("redirect", "/")

    user = discord.fetch_user()
    return redirect(redirect_to)


@auth.route("/me")
def me():
    user = discord.fetch_user()
    return f"""
<html>
<head>
<title>{user.name}</title>
</head>
<body><img src='{user.avatar_url or user.default_avatar_url}' />
<p>Is avatar animated: {str(user.is_avatar_animated)}</p>
<br />
</body>
</html>
"""
