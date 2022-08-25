import json
from flask import *
from db import Database, make_file
from handle_apikeys import *

db_campaigns = Database(make_file("data/db/campaigns.json"))

campaigns_api = Blueprint("campaigns_api", __name__)


@campaigns_api.route("/api/v1.0/campaigns/", methods=["GET"])
def get_campaigns():
    return jsonify(db_campaigns.get_all()), 200


@campaigns_api.route("/api/v1.0/campaigns/<int:key>/", methods=["GET"])
def get_campaign(key):
    if db_campaigns.has_key(key):
        return db_campaigns.get_key(key)
    abort(404)

@campaigns_api.route("/api/v1.0/campaigns/<int:key>/", methods=["PUT"])
def toggle_player(key):
    #   We update the player list and count by modifying an in-memory clone of the requested
    #   key-value-pair, and then updating the database when we are done. This saves disk activity.
    #   I think.
    request_player = str(request.args.get("player"))
    campaign: dict = db_campaigns.get_key(key)
    campaign_players: list = campaign["players"]
    campaign_players_count: int = campaign["players_current"]
    if request_player in campaign_players:
        campaign_players.remove(request_player)
        campaign.update({"players": campaign_players})
        campaign.update({"players_current": campaign_players_count - 1})
    else:
        campaign_players.append(request_player)
        campaign.update({"players": campaign_players})
        campaign.update({"players_current": campaign_players_count + 1})
    return json.dumps(db_campaigns.set_key(campaign, key), indent=4)

    
@campaigns_api.route("/api/v1.0/campaigns/", methods=["POST"])
def set_campaign():
    key = request.args.get("id")
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
