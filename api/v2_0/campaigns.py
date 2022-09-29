from api.v2_0.models import dbsql as db
from flask import Flask, Blueprint, abort, jsonify, request, views

campaigns = Blueprint("campaigns_api_v2", __name__)

@campaigns.route("/api/v2.0/campaigns/", methods=["GET"])
def get_all_campaigns():

