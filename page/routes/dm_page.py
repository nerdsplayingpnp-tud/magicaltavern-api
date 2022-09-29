from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from api.v1_0.campaigns import get_campaigns

dm_page = Blueprint("dm_page", __name__)


@dm_page.route("/DmPage")
@login_required
def DmPage():
    if not current_user.is_dm():
        return redirect(url_for("weblogic.index"))
    campaings = []
    campaigns_json = get_campaigns()[0].json
    for campaign in campaigns_json:
        camp = campaigns_json[campaign]
        if current_user.id == camp["dungeon_master"]:
            camp["key"] = campaign
            campaings.append(camp)
        if campaings == []:
            campaings = "You dont master any Campaigns right now"
    return render_template("DmPage.html", campaigns=campaings)
