from flask import Flask

# Fill in these values with the required settings


def configure(app: Flask) -> Flask:
    app.config["MAIL_SERVER"] = ""
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = ""
    app.config["MAIL_PASSWORD"] = ""
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = False
    app.config["SECRET_KEY"] = ""
    return app
