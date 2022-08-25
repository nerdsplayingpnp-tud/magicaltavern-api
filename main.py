from flask import *
from flask import Flask, render_template
from handle_apikeys import generate, validate, put
from pathlib import Path
from db import Database, make_file
from api.v1_0.campaigns import campaigns_api
import json, time
from api.v1_0.campaigns import get_campaigns, db_campaigns

app = Flask(__name__)
# Register the blueprint in api/v1_0/campaigns.py
app.register_blueprint(campaigns_api)


# Register a route
@app.route("/api/v1.0/", methods=["GET"])
def home_page():
    return json.dumps("API is online.")

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/campaigns')
def campaign_page():
    #get campaigns 
    
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
        "players": []
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
        "players": []
    }
    if (not db_campaigns.has_key(922031)) & (not db_campaigns.has_key(553841)):
        db_campaigns.set_key((camp1), 922031)
        db_campaigns.set_key((camp2), 553841)
    campaigns_json = get_campaigns()[0].json
    campaings = []
    for campaign in campaigns_json:
        campaings.append(campaigns_json[campaign])
    return render_template('campaigns.html', messages = campaings)

@app.route('/mentor')
def mentor_page():
    return render_template('dm_mentor.html')

@app.route('/impressum')
def impressum_page():
    return render_template('impressum.html')

if __name__ == "__main__":
    put(generate())
    app.run(port=7777)
