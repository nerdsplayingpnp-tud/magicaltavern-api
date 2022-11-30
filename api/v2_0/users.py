import bleach
from flask import Blueprint, request, jsonify, abort
from api.v2_0.authentication import abort_if_token_invalid
from api.v2_0.models import (
    User,
    ensure_player_exists,
    table_to_dict,
    does_campaign_exist,
    campaign_player_association,
    campaign_dm_association,
    Campaign,
)
from api.v2_0.models import dbsql as db

users = Blueprint("users", __name__)


@users.route("/api/v2.0/users/", methods=["GET"])
def get_all_users():
    abort_if_token_invalid(request)
    users = table_to_dict(User)
    for user in users:
        users[user].pop("id")
    return jsonify(users)


@users.route("/api/v2.0/users/<int:id>/", methods=["GET"])
def get_singular_user(id):
    abort_if_token_invalid(request)
    item = User.query.filter(User.id == id).one_or_none()
    if not item:
        abort(400, "This User does not exist.")
    item = item.to_dict()
    item.pop("id")
    return jsonify(item), 200


@users.route("/api/v2.0/users/<int:user_id>/plays_campaigns/", methods=["GET"])
def get_campaigns_where_player(user_id):
    abort_if_token_invalid(request)
    items = (
        Campaign.query.join(campaign_player_association)
        .filter((campaign_player_association.c.player == user_id))
        .all()
    )

    if not items:
        return (jsonify({})), 200
    returned_dict = {}
    for item in items:
        returned_dict[item.id] = item.to_dict()
        returned_dict[item.id].pop("id")

    return jsonify(returned_dict), 200


@users.route("/api/v2.0/users/<int:user_id>/dms_campaigns/", methods=["GET"])
def get_campaigns_where_dm(user_id):
    abort_if_token_invalid(request)
    items = (
        Campaign.query.join(campaign_dm_association)
        .filter((campaign_dm_association.c.dm == user_id))
        .all()
    )

    if not items:
        return (jsonify({})), 200
    returned_dict = {}
    for item in items:
        returned_dict[item.id] = item.to_dict()
        returned_dict[item.id].pop("id")

    return jsonify(returned_dict), 200


@users.route("/api/v2.0/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    abort_if_token_invalid(request)
    # TODO: Implement
