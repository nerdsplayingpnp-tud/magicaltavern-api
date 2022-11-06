from flask import Blueprint, Response
from api.v2_0.models import Campaign

campaigns_api_v2 = Blueprint("campaigns_api_v2", __name__)


@campaigns_api_v2.route("/api/v2.0/campaigns/", methods=["GET"])
def get_all_campaigns():
    query_campaigns = Campaign.query.all()
    return Response(status=404)  # TODO Implement
