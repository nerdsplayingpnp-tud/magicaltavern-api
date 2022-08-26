from flask import *
from db import Database, make_file
from handle_apikeys import validate

db_campaigns = Database(make_file("data/db/campaigns.json"))

campaigns_api = Blueprint("campaigns_api", __name__)


@campaigns_api.route("/api/v1.0/campaigns/", methods=["GET"])
def get_campaigns():
    if not validate(request.args.get("apikey")):
        abort(403)
    return jsonify(db_campaigns.get_all()), 200


@campaigns_api.route("/api/v1.0/campaigns/<int:key>/", methods=["GET"])
def get_campaign(key):
    if not validate(request.args.get("apikey")):
        abort(403)
    if db_campaigns.has_key(key):
        return db_campaigns.get_key(key), 200
    abort(404)


@campaigns_api.route("/api/v1.0/campaigns/<int:key>/player/", methods=["PUT"])
def toggle_player(key):
    #   We update the player list and count by modifying an in-memory clone of the requested
    #   key-value-pair, and then updating the database when we are done. This saves disk activity.
    #   I think.
    if not validate(request.args.get("apikey")):
        abort(403)
    request_player = str(request.args.get("player"))
    campaign: dict = db_campaigns.get_key(key)
    print(str(campaign))
    campaign_players: list = campaign["players"]
    campaign_players_count: int = campaign["players_current"]
    if request_player in campaign_players:
        campaign_players.remove(request_player)
        campaign.update({"players": campaign_players})
        campaign.update({"players_current": campaign_players_count - 1})
        db_campaigns.set_key(campaign, key)
        return "True"
    else:
        if campaign_players_count + 1 > campaign["players_max"]:
            abort(409, description="Too many players in this campaign.")
        campaign_players.append(request_player)
        campaign.update({"players": campaign_players})
        campaign.update({"players_current": campaign_players_count + 1})
        db_campaigns.set_key(campaign, key)
        return "False"


@campaigns_api.route("/api/v1.0/campaigns/<int:key>/has_view/", methods=["PUT"])
def confirm_view(key):
    #   We update the player list and count by modifying an in-memory clone of the requested
    #   key-value-pair, and then updating the database when we are done. This saves disk activity.
    #   I think.
    if not validate(request.args.get("apikey")):
        abort(403)
    campaign: dict = db_campaigns.get_key(key)
    if "has_view" in campaign.keys():
        campaign.update({"has_view": True})
        return jsonify(True)
    else:
        campaign.update({"has_view": False})
        return jsonify(False)


@campaigns_api.route("/api/v1.0/campaigns/", methods=["POST"])
def set_campaign():
    if not validate(request.args.get("apikey")):
        abort(403)
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
        if key_required not in request.json:
            abort(400)

    data_optional_or_preset = {
        "image_url": request.json.get("image_url", ""),
        "players_current": 0,
        "players": [],
        "has_view": False,
    }

    return_value = db_campaigns.set_key((data_required | data_optional_or_preset), key)
    return jsonify(return_value)
