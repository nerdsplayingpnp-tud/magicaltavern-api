from flask import Flask

# Fill in these values with the required settings


def configure(app: Flask) -> Flask:
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = "nerdsplaypnpvalidator@gmail.com"
    app.config["MAIL_PASSWORD"] = "xwebtezpptgxfcbs"  #'$52ceP^1xbMU'
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    app.config[
        "SECRET_KEY"
    ] = "e6405ba489b12b5c3e736e70094c315c85132c5cb16bd2c5cfbbbe47868bfe32"
    return app
