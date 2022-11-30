from flask import Flask

# Fill in these values with the required settings


def configure(app: Flask) -> Flask:
    app.config["SECRET_KEY"] = ""
    app.config["DISCORD_CLIENT_ID"] = 
    app.config["DISCORD_CLIENT_SECRET"] = ""
    app.config["DISCORD_REDIRECT_URI"] = ""
    return app
