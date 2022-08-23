from crypt import methods
from flask import *
from flask import Flask, render_template
from handle_apikeys import generate, validate, put
from pathlib import Path
from db import Database, make_file
from api.v1_0.campaigns import campaigns_api
import json, time

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
def index():
    #get campaigns 
    campaings = [{'title' : 'Campaign_One'},{'title' :'Campaign_two'}]
    return render_template('campaigns.html', messages = campaings)

if __name__ == "__main__":
    put(generate())
    app.run(port=7777)
