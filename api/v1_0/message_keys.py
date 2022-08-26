from crypt import methods
from flask import *
from db import Database, make_file
from handle_apikeys import validate

db_message_keys = Database(make_file("data/db/message_keys.json"))

message_keys = Blueprint("message_keys", __name__)


@message_keys.route("/api/v1.0/message_keys/", methods=["GET"])
def get_all():
    return jsonify(db_message_keys.get_all()), 200

@message_keys.route("/api/v1.0/message_keys/<int:key>", methods=["GET"])
def get_key(key):
    if db_message_keys.has_key(key):
        return jsonify(db_message_keys.get_key(key)), 200
    abort(404)

@message_keys.route("/api/v1.0/message_keys/", methods=["POST"])
def post_key_messageid():
    if not validate(request.args.get("apikey")):
        abort(403, description="Invalid or missing API key.")
    message_id = request.args.get("messageid")
    key = request.args.get("db_key")
    if key is None or message_id is None:
        abort(400, description="One or more arguments not given.")
    if message_id in db_message_keys.get_all().keys():
        abort(400, description="messageid already has a db_key in the database.")
    db_message_keys.set_key(str(key), str(message_id))
    return jsonify(True), 200
