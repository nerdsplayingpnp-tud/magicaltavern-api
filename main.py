from wsgiref.util import request_uri
from flask import *
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from flask_mail import Mail, Message
from handle_apikeys import generate, put
from pathlib import Path
from db import Database, make_file
import json, time
from api.v1_0.campaigns import get_campaigns, db_campaigns, toggle_player
from db import dbsql as db

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nerdsplaypnpvalidator@gmail.com'
app.config['MAIL_PASSWORD'] = 'xwebtezpptgxfcbs' #'$52ceP^1xbMU'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KEY'] = 'e6405ba489b12b5c3e736e70094c315c85132c5cb16bd2c5cfbbbe47868bfe32'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
mail = Mail(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
# Register a route
@app.route("/api/v1.0/", methods=["GET"])
def home_page():
    return json.dumps("API is online.")

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
    user = User.query.filter_by(email=email).first()
    user.email_confirm = True
    db.session.commit()
    flash('Your Email has been confirmed!')
    return  redirect(url_for('auth.login'))

@app.route('/reset_password/<token>', methods=["GET","POST"])
def resetPassword(token):
    if request.method == 'GET':
    #verify token
        try:
                s = URLSafeTimedSerializer(
                    current_app.config["SECRET_KEY"], salt="password-reset"
                )
                email = s.loads(token, salt="password-reset", max_age=3600)
        except (SignatureExpired, BadSignature):
                return render_template("error.html")
        user = User.query.filter_by(email=email).first()
        return  render_template('reset_password.html', token=token)
    if request.method == 'POST':
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')
        try:
            s = URLSafeTimedSerializer(
                current_app.config["SECRET_KEY"], salt="password-reset"
            )
            email = s.loads(token, salt="password-reset", max_age=3600)
        except (SignatureExpired, BadSignature):
            return render_template("error.html")
        if password == passwordConfirm:
            user = User.query.filter_by(email=email).first()
            user.password = generate_password_hash(password, method='sha256')
            db.session.commit()
        else:
            flash('Passwords werent the same!')
            return  redirect('/reset_password/' + token)
        flash('New Password has been set')
        return redirect(url_for('auth.login'))

#@app.route('/validate', methods=["POST"])
#no reason right now for this to be callable from outside
def validate(email):
    s = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"], salt="email-comfirm"
        )
    token = s.dumps(email, salt="email-confirm")
    msg = Message('PnP Email Authentication', sender =   ("Nerds Play PnP", 'nerdsplaypnpvalidator@gmail.com'), recipients = [email])
    msg.body = "Hello Adventurer, ready for your next Adventure? Click the link to confirm your Email: " + request.url_root + url_for('confirm_Email', token = token)
    mail.send(msg)
    return None

@app.route('/reset_password', methods=['POST', 'GET'])
def reset_password_mail():
    if request.method == 'GET':
        return render_template('reset_password_mail.html')
    if request.method == 'POST':
        email = request.form.get('email')
        s = URLSafeTimedSerializer(
                current_app.config["SECRET_KEY"], salt="password-reset"
            )
        token = s.dumps(email, salt="password-reset")
        msg = Message('PnP Email Authentication', sender =   ("Nerds Play PnP", 'nerdsplaypnpvalidator@gmail.com'), recipients = [email])
        msg.body = "Hello Adventurer, click the link to reset your password:" + request.url_root + url_for('resetPassword', token = token)
        mail.send(msg)
        flash('Please check your Inbox')
        return redirect(url_for('auth.login'))
    

from api.v1_0.models import User
@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

if __name__ == "__main__":
    put(generate())
    #Register all the blueprints
    from api.v1_0.auth import auth
    from api.v1_0.website_logic import weblogic
    from api.v1_0.campaigns import campaigns_api
 
    app.register_blueprint(campaigns_api)
    app.register_blueprint(weblogic)
    app.register_blueprint(auth)
    app.run(port=7777, debug=True)
