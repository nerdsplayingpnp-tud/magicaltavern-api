from flask import *
from handle_apikeys import validate
from pathlib import Path
from db import Database, make_file
import json, time

app = Flask(__name__)

# example_dict = {
#     1: {"name": "2", "min_players": 1, "max_players": 5, "description": "lorem ipsum"},
#     2: {"name": "1", "min_players": 2, "max_players": 5, "description": "lorem ipsum"},
#     3: {"name": "3", "min_players": 3, "max_players": 5, "description": "lorem ipsum"},
# }

# print(example_dict.get(1))


@app.route("/api/", methods=["GET"])
def home_page():
    data_set = {
        "Page": "Home",
        "Message": "Loaded Homepage.",
        "Current Time": time.time(),
    }
    return json.dumps(data_set)


@app.route("/api/v1.0/campaigns/", methods=["GET"])
def get_campaigns():
    user_query = str(request.args.get("user"))  #  /user/?user=HASJK4AF_NAME

    data_set = {
        "Page": "Request",
        "Message": f"Request: {user_query}",
        "Time": time.time(),
    }
    return json.dumps(data_set)


if __name__ == "__main__":
    example_data = {"name": "yes", "players": 3542343}
    validate("a")
    campaigns = Database(make_file("data/db/campaigns.json"))
    campaigns.set_key(example_data, 2)
    print(campaigns.get_key("1"))
    app.run(port=7777)
