from flask import Blueprint, request, jsonify, escape, abort
from api.v2_0.authentication import abort_if_token_invalid
from api.v2_0.models import (
    table_to_dict,
    Campaign,
    ensure_player_exists,
    User,
    campaign_player_association,
    campaign_dm_association,
)
from api.v2_0.models import dbsql as db


campaigns_api_v2 = Blueprint("campaigns_api_v2", __name__)


@campaigns_api_v2.route("/api/v2.0/campaigns/", methods=["GET"])
def get_all_campaigns():
    abort_if_token_invalid(request)
    return jsonify(table_to_dict(Campaign)), 200


@campaigns_api_v2.route("/api/v2.0/campaigns/", methods=["POST"])
def add_new_campaign():
    abort_if_token_invalid(request)
    new_campaign = Campaign()
    request_json: dict = request.json
    if len(str(request_json)) >= 10000:
        abort(400, "Request too big.")
    try:
        new_campaign = Campaign(
            name=escape(request_json["name"]),
            description=escape(request_json["description"]),
            players_min=escape(request_json["players_min"]),
            players_max=escape(request_json["players_max"]),
            complexity=escape(request_json["complexity"]),
            place=escape(request_json["place"]),
            time=escape(request_json["time"]),
            content_warnings=escape(request_json["content_warnings"]),
            ruleset=escape(request_json["ruleset"]),
            campaign_length=escape(request_json["campaign_length"]),
            language=escape(request_json["language"]),
            character_creation=escape(request_json["character_creation"]),
            briefing=escape(request_json["briefing"]),
            notes=escape(request_json["notes"]),
            image_url=escape(request_json.get("image_url")),
        )
        db.session.add(new_campaign)
        db.session.commit()
    except KeyError:
        abort(
            400,
            "Your request does not contain all required values. Please, consult the API documentation.",
        )
    return jsonify(new_campaign.id), 200


@campaigns_api_v2.route("/api/v2.0/campaigns/<int:id>", methods=["GET"])
def get_singular_campaign(id):
    abort_if_token_invalid(request)
    item = Campaign.query.filter(Campaign.id == id).one_or_none()
    if not item:
        abort(400, "This Campaign does not exist.")
    return jsonify(item.to_dict()), 200


@campaigns_api_v2.route(
    "/api/v2.0/campaigns/<int:campaign_id>/players", methods=["GET"]
)
def get_players_from_campaign(campaign_id):
    abort_if_token_invalid(request)
    campaign = Campaign.query.filter(Campaign.id == campaign_id).one_or_none()
    if not campaign:
        abort(400, "This Campaign does not exist.")
    items = (
        User.query.join(campaign_player_association)
        .join(Campaign)
        .filter(
            (campaign_player_association.c.player == User.id)
            & (campaign_player_association.c.campaign == campaign_id)
        )
        .all()
    )
    if not items:
        return (jsonify({})), 200
    returned_dict = {}
    for item in items:
        returned_dict[item.id] = item.to_dict()
        returned_dict[item.id].pop("id")

    return jsonify(returned_dict), 200


@campaigns_api_v2.route("/api/v2.0/campaigns/<int:campaign_id>/dm", methods=["GET"])
def get_dm_from_campaign(campaign_id):
    abort_if_token_invalid(request)
    campaign = Campaign.query.filter(Campaign.id == campaign_id).one_or_none()
    if not campaign:
        abort(400, "This Campaign does not exist.")
    items = (
        User.query.join(campaign_dm_association)
        .join(Campaign)
        .filter(
            (campaign_dm_association.c.dm == User.id)
            & (campaign_dm_association.c.campaign == campaign_id)
        )
        .all()
    )
    if not items:
        return (jsonify({})), 200
    returned_dict = {}
    for item in items:
        returned_dict[item.id] = item.to_dict()
        returned_dict[item.id].pop("id")

    return jsonify(returned_dict), 200


@campaigns_api_v2.route(
    "/api/v2.0/campaigns/<int:campaign_id>/players/add/<int:user_id>", methods=["PUT"]
)
def add_player_to_campaign(campaign_id, user_id):
    abort_if_token_invalid(request)
    user_from_id = ensure_player_exists(user_id)
    campaign = Campaign.query.filter(Campaign.id == campaign_id).one_or_none()
    if not campaign:
        abort(400, "This Campaign does not exist.")
    if user_from_id in campaign.players:
        abort(409, "The player is already in this campaign.")
    campaign.players.append(user_from_id)
    db.session.commit()
    return jsonify("Success"), 201


@campaigns_api_v2.route(
    "/api/v2.0/campaigns/<int:campaign_id>/players/remove/<int:user_id>",
    methods=["PUT"],
)
def remove_player_from_campaign(campaign_id, user_id):
    abort_if_token_invalid(request)
    user_from_id = ensure_player_exists(user_id)
    campaign = Campaign.query.filter(Campaign.id == campaign_id).one_or_none()
    if not campaign:
        abort(400, "This Campaign does not exist.")
    if user_from_id not in campaign.players:
        abort(409, "The player is not in this campaign.")
    campaign.players.remove(user_from_id)
    db.session.commit()
    return jsonify("Success"), 201
