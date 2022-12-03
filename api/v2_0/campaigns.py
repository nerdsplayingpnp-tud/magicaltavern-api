import bleach
from flask import Blueprint, request, jsonify, abort, escape
from api.v2_0.authentication import abort_if_token_invalid
from api.v2_0.models import (
    table_to_dict,
    Campaign,
    ensure_player_exists,
    User,
    campaign_player_association,
    campaign_dm_association,
    does_campaign_exist,
    campaign_not_finished,
    campaign_cannot_be_active,
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
        abort(413, "Request too big.")
    try:
        new_campaign = Campaign(
            name=bleach.clean(request_json["name"]),
            description=bleach.clean(request_json["description"]),
            players_min=escape(request_json["players_min"]),
            players_max=escape(request_json["players_max"]),
            complexity=escape(request_json["complexity"]),
            place=bleach.clean(request_json["place"]),
            time=bleach.clean(request_json["time"]),
            content_warnings=bleach.clean(request_json["content_warnings"]),
            ruleset=escape(request_json["ruleset"]),
            campaign_length=escape(request_json["campaign_length"]),
            language=escape(request_json["language"]),
            character_creation=bleach.clean(request_json["character_creation"]),
            briefing=bleach.clean(request_json["briefing"]),
            notes=bleach.clean(request_json["notes"]),
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
    does_campaign_exist(request, campaign_id)
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
    does_campaign_exist(request, campaign_id)
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
    campaign_cannot_be_active(request, campaign_id)
    campaign_not_finished(request, campaign_id)
    user_from_id = ensure_player_exists(user_id)
    campaign = does_campaign_exist(request, campaign_id)
    if user_from_id in campaign.players:
        abort(409, "The player is already in this campaign.")
    if user_from_id in campaign.dm:
        abort(409, "A DM cannot be player in their own campaign.")
    if len(campaign.players) >= campaign.players_max:
        abort(409, "The campaign is full.")
    campaign.players.append(user_from_id)
    db.session.commit()
    return jsonify("Success"), 201


@campaigns_api_v2.route(
    "/api/v2.0/campaigns/<int:campaign_id>/players/remove/<int:user_id>",
    methods=["PUT"],
)
def remove_player_from_campaign(campaign_id, user_id):
    abort_if_token_invalid(request)
    campaign_cannot_be_active(request, campaign_id)
    campaign_not_finished(request, campaign_id)
    user_from_id = ensure_player_exists(user_id)
    campaign = does_campaign_exist(request, campaign_id)
    if user_from_id not in campaign.players:
        abort(409, "The player is not in this campaign.")
    campaign.players.remove(user_from_id)
    db.session.commit()
    return jsonify("Success"), 201


@campaigns_api_v2.route(
    "/api/v2.0/campaigns/<int:campaign_id>/dm/add/<int:user_id>", methods=["PUT"]
)
def add_dm_to_campaign(campaign_id, user_id):
    abort_if_token_invalid(request)
    campaign_not_finished(request, campaign_id)
    user_from_id = ensure_player_exists(user_id)
    if not user_from_id.is_dm():
        abort(400, "Supplied user lacks access level to be DM of a campaign.")
    campaign = does_campaign_exist(request, campaign_id)
    if user_from_id in campaign.dm:
        abort(409, "The player is already DM of this campaign.")
    if campaign.dm != []:
        abort(409, "The campaign already has a DM.")
    campaign.dm = [user_from_id]
    db.session.commit()
    return jsonify("Success"), 201


@campaigns_api_v2.route(
    "/api/v2.0/campaigns/<int:campaign_id>/dm/remove/<int:user_id>", methods=["PUT"]
)
def remove_dm_from_campaign(campaign_id, user_id):
    abort_if_token_invalid(request)
    campaign_not_finished(request, campaign_id)
    user_from_id = ensure_player_exists(user_id)
    campaign = does_campaign_exist(request, campaign_id)
    if user_from_id not in campaign.dm:
        abort(409, "The player already isn't DM of this campaign.")
    campaign.dm = []
    db.session.commit()
    return jsonify("Success"), 201


@campaigns_api_v2.route(
    "/api/v2.0/campaigns/<int:campaign_id>/message_id/<int:message_id>", methods=["PUT"]
)
def add_message_id_to_campaign(message_id, campaign_id):
    abort_if_token_invalid(request)
    campaign_not_finished(request, campaign_id)
    campaign = does_campaign_exist(request, campaign_id)
    campaign.message_id = message_id
    db.session.commit()
    return jsonify("Success"), 200


@campaigns_api_v2.route(
    "/api/v2.0/campaigns/<int:campaign_id>/message_id/", methods=["GET"]
)
def get_message_id_from_campaign(campaign_id):
    abort_if_token_invalid(request)
    campaign = does_campaign_exist(request, campaign_id)
    return jsonify(campaign.message_id), 200


@campaigns_api_v2.route(
    "/api/v2.0/campaigns/<int:campaign_id>/activate", methods=["PUT"]
)
def activate_campaign(campaign_id):
    abort_if_token_invalid()
    campaign = does_campaign_exist(request, campaign_id)
    if campaign.active == True:
        abort(409, "The campaign is already marked as active.")
    campaign.active = True
    db.session.commit()
    return jsonify("Success."), 200


@campaigns_api_v2.route("/api/v2.0/campaigns/<int:campaign_id>/finish", methods=["PUT"])
def finish_campaign(campaign_id):
    abort_if_token_invalid()
    campaign = does_campaign_exist(request, campaign_id)
    if campaign.finished == True:
        abort(409, "The campaign is already marked as finished.")
    campaign.finished = True
    db.session.commit()
    return jsonify("Success."), 200
