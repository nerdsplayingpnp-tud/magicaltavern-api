import bleach
from flask import Blueprint, request, jsonify, abort
from api.v2_0.authentication import abort_if_token_invalid
from api.v2_0.models import (
    table_to_dict,
    Ruleset,
)
from api.v2_0.models import dbsql as db


rulesets = Blueprint("rulesets", __name__)


@rulesets.route("/api/v2.0/rulesets/add/", methods=["POST"])
def create_ruleset():
    abort_if_token_invalid(request)
    request_json: dict = request.json
    converted = str()
    for key in request_json:
        converted += request_json[key]
    if len(converted) >= 50:
        abort(413, "Request too large.")
    try:
        new_ruleset = Ruleset(ruleset=bleach.clean(str(converted)))
        db.session.add(new_ruleset)
        db.session.commit()
    except KeyError:
        abort(
            400,
            "Your request does not contain all required values. Please, consult the API documentation.",
        )
    return jsonify(new_ruleset.id), 200


@rulesets.route("/api/v2.0/rulesets/", methods=["GET"])
def get_all_rulesets():
    abort_if_token_invalid(request)
    return jsonify(table_to_dict(Ruleset)), 200


@rulesets.route("/api/v2.0/rulesets/<int:id>")
def get_ruleset_by_id(id):
    abort_if_token_invalid(request)
    item = Ruleset.query.filter(Ruleset.id == id).one_or_none()
    if not item:
        abort(400, "This Ruleset does not exist.")
    item = item.to_dict()
    item.pop("id")
    return jsonify(item), 200
