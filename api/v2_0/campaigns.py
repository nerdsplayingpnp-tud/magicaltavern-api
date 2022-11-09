from flask import Blueprint, request, jsonify, escape, abort
from api.v2_0.authentication import abort_if_token_invalid
from api.v2_0.models import table_to_dict, Campaign
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
            "Your request does not contain all required valued. Please, consult the API documentation.",
        )
    return jsonify(new_campaign.id), 200


@campaigns_api_v2.route("/api/v2.0/campaigns/<int:id>", methods=["GET"])
def get_singular_campaign(id):
    abort_if_token_invalid(request)
    item = Campaign.query.filter(Campaign.id == id).one()
    return jsonify(item.to_dict()), 200
