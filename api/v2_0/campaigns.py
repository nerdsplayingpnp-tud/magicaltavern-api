from api.v2_0.models import dbsql as db
from flask import Flask, Blueprint, abort, jsonify, request, views
from api.v2_0.models import Campaign

campaigns_api_v2 = Blueprint("campaigns_api_v2", __name__)


@campaigns_api_v2.route("/api/v2.0/campaigns/", methods=["GET"])
def get_all_campaigns():
    query_campaigns = Campaign.query.all()
    return jsonify(query_campaigns), 200
