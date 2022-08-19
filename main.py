from crypt import methods
from flask import *
from handle_apikeys import generate, validate, put
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

db_campaigns = Database(make_file("data/db/campaigns.json"))


@app.route("/api/v1.0/", methods=["GET"])
def home_page():
    return json.dumps("API is online.")


@app.route("/api/v1.0/campaigns/", methods=["GET"])
def get_campaigns():
    return jsonify(db_campaigns.get_all()), 200


@app.route("/api/v1.0/campaigns/<int:key>/", methods=["GET"])
def get_campaign(key):
    if db_campaigns.has_key(key):
        return db_campaigns.get_key(key)
    abort(404)


@app.route("/api/v1.0/campaigns/", methods=["POST"])
def set_campaign():
    key = request.args.get("id")
    print("Entering the FUNK 🪩🕺")
    data_required = {
        "name": request.json["name"],
        "dungeon_master": request.json["dungeon_master"],
        "description": request.json["description"],
        "players_min": request.json["players_min"],
        "players_max": request.json["players_max"],
        "complexity": request.json["complexity"],
        "place": request.json["place"],
        "time": request.json["time"],
        "content_warnings": request.json["content_warnings"],
        "ruleset": request.json["ruleset"],
        "campaign_length": request.json["campaign_length"],
        "language": request.json["language"],
        "character_creation": request.json["character_creation"],
        "briefing": request.json["briefing"],
        "notes": request.json["notes"],
    }
    if not request.json:
        abort(400)

    for key_required in data_required.keys():
        if key_required not in request.json or not validate(request.args.get("apikey")):
            abort(400)

    data_optional_or_preset = {
        "image_url": request.json.get("image_url", ""),
        "players_current": 0,
        "players": [],
    }

    return json.dumps(
        db_campaigns.set_key((data_required | data_optional_or_preset), key), indent=4
    )


if __name__ == "__main__":
    app.run(port=7777)
