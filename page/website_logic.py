from flask import *
from handle_apikeys import *

from api.v1_0.campaigns import get_campaigns, db_campaigns
from db import dbsql as db
from flask_login import login_required, current_user
from page.models import User, Ruleset, MentorProgramm


weblogic = Blueprint("weblogic", __name__)


@weblogic.route("/")
def index():
    return render_template("index.html")


@weblogic.route("/profile")
@login_required
def profile():
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


@weblogic.route("/DmPage")
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


@weblogic.route("/AdminPage")
@login_required
def AdminPage():
    if not current_user.is_admin():
        return redirect(url_for("weblogic.index"))
    users = User.query.all()
    return render_template("AdminPage.html", users=users)


@weblogic.route("/campaigns", methods=["GET"])
def campaign_page():
    # get campaigns

    camp1 = {
        "name": "test",
        "dungeon_master": 261192665247252480,
        "description": "test",
        "players_min": 1,
        "players_max": 4,
        "complexity": "Einsteigerfreundlich",
        "place": "Online",
        "time": "a",
        "content_warnings": "a",
        "ruleset": "a",
        "campaign_length": "Oneshot (1-2 Sessions)",
        "language": "Englisch",
        "character_creation": "a",
        "briefing": "a",
        "notes": "a",
        "players_current": 0,
        "players": [],
    }

    camp2 = {
        "name": "Test 2",
        "dungeon_master": 261192665247252480,
        "description": "Dies ist eine Beschreibung. Beschreibungen k\u00f6nnen recht lang sein, deswegen mache ich sie auch lang. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "players_min": 1,
        "players_max": 10,
        "complexity": "Fortgeschritten",
        "place": "Online",
        "time": "To be Decided",
        "content_warnings": "None",
        "ruleset": "DnD 5E",
        "campaign_length": "L\u00e4ngere Kampagne (7+ Sessions)",
        "language": "Englisch",
        "character_creation": "Vorher erstellen, Level 7 Charaktere",
        "briefing": "Ja",
        "notes": "N\u00f6",
        "players_current": 0,
        "players": [],
    }
    if (not db_campaigns.has_key(922031)) & (not db_campaigns.has_key(553841)):
        db_campaigns.set_key((camp1), 922031)
        db_campaigns.set_key((camp2), 553841)
    campaigns_json = get_campaigns()[0].json
    campaings = []
    for campaign in campaigns_json:
        camp = campaigns_json[campaign]
        camp["key"] = campaign
        campaings.append(camp)
    return render_template("campaigns.html", campaigns=campaings)


@weblogic.route("/mentor", methods=["GET"])
def mentor_page():
    rulesets = Ruleset.query.all()
    if not rulesets:
        ruleset = Ruleset(ruleset="DnD 5th Edition")
        db.session.add(ruleset)
        db.session.commit()
    programms = MentorProgramm.query.all()
    openProgramms = []
    mentoredProgramms = []
    if current_user.is_authenticated:
        for programm in programms:
            if not programm.mentorId:
                openProgramms.append(programm)
            if programm.mentorId == current_user.id:
                mentoredProgramms.append(programm)
    return render_template(
        "dm_mentor.html",
        rulesets=rulesets,
        openProgramms=openProgramms,
        mentoredProgramms=mentoredProgramms,
    )


@weblogic.route("/impressum", methods=["GET"])
def impressum_page():
    return render_template("impressum.html")
