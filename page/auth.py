import bleach
from main import discord, app
from flask import Blueprint, redirect, abort
from flask_discord import DiscordOAuth2Session
from api.v2_0.models import dbsql as db
from api.v2_0.models import ensure_player_exists

auth = Blueprint("auth", __name__)


def requires_authorization(discord: DiscordOAuth2Session):
    with app.app_context():
        if not discord.authorized:
            abort(401)
        else:
            return discord.fetch_user()


@auth.route("/login")
def login():
    return discord.create_session()


@auth.route("/logout")
def logout():
    discord.revoke()
    return redirect("/")


@auth.route("/callback")
def callback():
    discord.callback()
    user_discord = discord.fetch_user()
    user_database = ensure_player_exists(user_discord.id)
    user_database.name = bleach.clean(user_discord.name)
    db.session.commit()
    return redirect("/me")


@auth.route("/me")
def me():
    user = requires_authorization(discord)
    return f"""
<html>
<head>
<title>{user.name}</title>
</head>
<body><img src='{user.avatar_url or user.default_avatar_url}' />
<p>Is avatar animated: {str(user.is_avatar_animated)}</p>
<p>Access Level: {str(ensure_player_exists(user.id).access)}
<br />
</body>
</html>
"""
