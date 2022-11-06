from api.v2_0.models import dbsql as db
from flask import Flask, Blueprint, abort, jsonify, request, views, Response
from api.v2_0.models import Campaign, to_dict

campaigns_api_v2 = Blueprint("campaigns_api_v2", __name__)


@campaigns_api_v2.route("/api/v2.0/campaigns/", methods=["GET"])
def get_all_campaigns():
    query_campaigns = Campaign.query.all()
    return Response(status=404)  # TODO Implement
