from flask import Blueprint, render_template
from flask_login import current_user, login_required
from api.v1_0.campaigns import db_campaigns, get_campaigns

profile = Blueprint("profile", __name__)


@profile.route("/profile")
@login_required
def get_profile():
    campaign_names_player = []
    campaign_names_master = []
    campaigns_json = get_campaigns()[0].json
    for campaign in campaigns_json:
        camp = campaigns_json[campaign]
        if current_user.email in camp["players"]:
            campaign_names_player.append(camp["name"])
        if current_user.id == camp["dungeon_master"]:
            campaign_names_master.append(camp["name"])
    if campaign_names_player == []:
        campaign_names_player = "None"
    if campaign_names_master == []:
        campaign_names_master = "None"
    return render_template(
        "profile.html",
        user=current_user,
        campaign_names_player=campaign_names_player,
        campaign_names_master=campaign_names_master,
    )
