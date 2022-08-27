from wsgiref.util import request_uri
from flask import *
from flask import Flask, render_template
from handle_apikeys import generate, validate, put
from pathlib import Path
from db import Database, make_file
from api.v1_0.campaigns import campaigns_api
import json, time
from api.v1_0.campaigns import get_campaigns, db_campaigns, toggle_player

from flask_mail import Mail, Message

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature


app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nerdsplaypnpvalidator@gmail.com'
app.config['MAIL_PASSWORD'] = 'xwebtezpptgxfcbs' #'$52ceP^1xbMU'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KEY'] = "test"

mail = Mail(app)

# Register the blueprint in api/v1_0/campaigns.py
app.register_blueprint(campaigns_api)

# Register a route
@app.route("/api/v1.0/", methods=["GET"])
def home_page():
    return json.dumps("API is online.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirm_email/<token>', methods=["GET"])
def confirm_Email(token):
    #verify token
    try:
            s = URLSafeTimedSerializer(
                current_app.config["SECRET_KEY"], salt="email-confirm"
            )
            email = s.loads(token, salt="email-confirm", max_age=3600)
    except (SignatureExpired, BadSignature):
            return render_template("error.html")
    #toggle_player(key)
    return render_template("mail_welcome_confirm.html")
    flash(
            f"Your email has been verified and you can now login to your account",
            "success",
        )
    return redirect(url_for('campaign_page'))

@app.route('/validate', methods=["POST"])
def validate():
    email = request.form['email']
    s = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"], salt="email-comfirm"
        )
    token = s.dumps(email, salt="email-confirm")
    msg = Message('PnP Email Authentication', sender =   ("Nerds Play PnP", 'nerdsplaypnpvalidator@gmail.com'), recipients = [email])
    msg.body = "Hello Adventurer, ready for your next Adventure? Click the link to confirm your Email: " + request.url_root + url_for('confirm_Email', token = token)
    mail.send(msg)
    return redirect(url_for('campaign_page'))
    
@app.route('/campaigns', methods=["GET"])
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

@app.route('/mentor', methods=["GET"])
def mentor_page():
    return render_template('dm_mentor.html')

@app.route('/impressum', methods=["GET"])
def impressum_page():
    return render_template('impressum.html')

if __name__ == "__main__":
    put(generate())
    app.run(port=7777, debug=True)
