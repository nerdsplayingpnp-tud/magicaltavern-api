from crypt import methods
from flask import *
from handle_apikeys import generate, validate, put
from pathlib import Path
from db import Database, make_file
from api.v1_0.campaigns import campaigns_api
from api.v1_0.message_keys import message_keys
import json, time

app = Flask(__name__)
# Register the blueprint in api/v1_0/campaigns.py
app.register_blueprint(campaigns_api)
app.register_blueprint(message_keys)


# Register a route
@app.route("/api/v1.0/", methods=["GET"])
def home_page():
    return json.dumps("API is online.")


if __name__ == "__main__":
    validate(None)  #    Ensures that keys.txt exists.
    app.run(port=7777)
