from crypt import methods
from flask import *
from handle_apikeys import generate, validate, put
from pathlib import Path
from db import Database, make_file
from api.v1_0.campaigns import campaigns_api
import json, time

app = Flask(__name__)
app.register_blueprint(campaigns_api)

# example_dict = {
#     1: {"name": "2", "min_players": 1, "max_players": 5, "description": "lorem ipsum"},
#     2: {"name": "1", "min_players": 2, "max_players": 5, "description": "lorem ipsum"},
#     3: {"name": "3", "min_players": 3, "max_players": 5, "description": "lorem ipsum"},
# }

# print(example_dict.get(1))


@app.route("/api/v1.0/", methods=["GET"])
def home_page():
    return json.dumps("API is online.")


if __name__ == "__main__":
    app.run(port=7777)
