from flask import Blueprint, render_template
from api.v1_0.campaigns import db_campaigns, get_campaigns

campaigns = Blueprint("campaigns", __name__)


@campaigns.route("/campaigns", methods=["GET"])
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
    campaigns_list = []
    for campaign in campaigns_json:
        camp = campaigns_json[campaign]
        camp["key"] = campaign
        campaigns_list.append(camp)
    return render_template("campaigns.html", campaigns=campaigns_list)
