from wsgiref.util import request_uri
from werkzeug.security import generate_password_hash, check_password_hash
from flask import *
from flask_login import LoginManager, current_user,login_user, login_required, logout_user
from flask_mail import Mail, Message
from handle_apikeys import generate, put
from pathlib import Path
from db import Database, make_file, dbsql as db
import json, time
from api.v1_0.campaigns import get_campaigns, db_campaigns, toggle_player_web


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

@app.route('/confirm_email_campaign/<token>/<key>', methods=["GET"])
def confirm_Email_campaign(token,key):
    #verify token
    try:
            s = URLSafeTimedSerializer(
                current_app.config["SECRET_KEY"], salt="camp-confirm"
            )
            email = s.loads(token, salt="camp-confirm", max_age=3600)
    except (SignatureExpired, BadSignature):
            return render_template("error.html")
    user = User.query.filter_by(email=email).first()
    if not user.email_confirm:
        user.email_confirm = True
        db.session.commit()
    login_user(user)
    toggle_player_web(key)
    logout_user()
    flash('You have been signed up!')
    return  redirect(url_for('weblogic.campaign_page'))

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

@app.route('/signUpCampaign/<key>', methods=["POST"])
@login_required
def signUpCampaign(key):
    toggle_player_web(key)
    flash('You have been signed up for this campaign')
    return redirect(url_for('weblogic.campaign_page'))

@app.route('/signUpCampaignEmail/<key>', methods=["POST"])
def signUpCampaignEmail(key):
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        if user.is_guest():
            validateCampaign(email, key)
            flash('You need to confirm your Email Address, check your inbox')
            return redirect(url_for('weblogic.campaign_page'))
        else:
            flash("Error account with email exists, please sign in")
            return redirect(url_for('auth.login'))
    else:
        new_guest = User(email=email, name='guest', password=generate_password_hash('password', method='sha256'), email_confirm = False, access = 0)
        db.session.add(new_guest)
        db.session.commit()
        validateCampaign(email, key)
        flash('You need to confirm your Email Address, check your inbox')
        return redirect(url_for('weblogic.campaign_page'))

#@app.route('/validate', methods=["POST"])
#no reason right now for this to be callable from outside
#functions sends email for Account sign up authentication with appropriate salt and token
def validate(email):
    s = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"], salt="email-comfirm"
        )
    token = s.dumps(email, salt="email-confirm")
    msg = Message('PnP Email Authentication', sender =   ("Nerds Play PnP", 'nerdsplaypnpvalidator@gmail.com'), recipients = [email])
    msg.body = "Hello Adventurer, to complete the signup you have to confirm your email. Click the link to confirm your Email: " + request.url_root + url_for('confirm_Email', token = token)
    mail.send(msg)
    return None

#Use User name as Salt to not allow changing of Id to change email of another account
def validateNewEmail(email, id, name):
    s = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"], salt=name
        )
    token = s.dumps(email, salt=name)
    msg = Message('PnP Email Authentication', sender =   ("Nerds Play PnP", 'nerdsplaypnpvalidator@gmail.com'), recipients = [email])
    msg.body = "Hello Adventurer, to change your Email you have to confirm your new Email. Click the link to confirm your Email: " + request.url_root + url_for('confirm_new_Email', token = token, id=id)
    mail.send(msg)
    return None

def validateCampaign(email, key):
    s = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"], salt="camp-comfirm"
        )
    token = s.dumps(email, salt="camp-confirm")
    msg = Message('PnP Email Authentication', sender =   ("Nerds Play PnP", 'nerdsplaypnpvalidator@gmail.com'), recipients = [email])
    msg.body = "Hello Adventurer, ready for your next Adventure? Click the link to confirm your Email: " + request.url_root + url_for('confirm_Email_campaign', token = token, key = key)
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


@app.route('/changeName', methods=['GET', 'POST'])
@login_required
def change_Name():
    if request.method == 'GET':
        return render_template( 'profile.html', user=current_user, changeName = True)
    if request.method == 'POST':
        name = request.form.get('newName')
        user = User.query.filter_by(id=current_user.id).first()
        user.name = name
        db.session.commit()
        flash("New Name has been set!")
        return redirect(url_for( 'weblogic.profile'))

@app.route('/changeEmail', methods=['GET', 'POST'])
@login_required
def change_Email():
    if request.method == 'GET':
        return render_template( 'profile.html', user=current_user, changeEmail = True)
    if request.method == 'POST':
        email = request.form.get('email')
        validateNewEmail(email, current_user.id, current_user.name)
        flash("Please check your Inbox to confirm your new Email.")
        return redirect(url_for( 'weblogic.profile'))

#Check if user name is the right salt, to see if the ID has been tempered with
@app.route('/confirm_new_Email/<token>/<id>', methods=['GET'])
def confirm_new_Email(token, id):
    user = User.query.filter_by(id=id).first()
    
    try:
            s = URLSafeTimedSerializer(
                current_app.config["SECRET_KEY"], salt=user.name
            )
            email = s.loads(token, salt=user.name, max_age=3600)
    except (SignatureExpired, BadSignature):
            return render_template("error.html")
    user.email = email
    db.session.commit()
    flash('Your Email has been changed!')
    return  redirect(url_for('weblogic.profile'))

#Use Salt of User name to not allow changing of Id to change email of another account
@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def change_Password():
    if request.method == 'GET':
        return render_template( 'profile.html', user=current_user, changePassword = True)
    if request.method == 'POST':
        oldPass = request.form.get('oldPassword')
        newPass = request.form.get('newPassword')
        user = User.query.filter_by(id=current_user.id).first()
        if not check_password_hash(user.password, oldPass):
            flash("wrong password")
            return redirect(url_for( 'weblogic.profile'))
        user.password = generate_password_hash(newPass, method='sha256')
        db.session.commit()
        flash("New Password has been set!")
        return redirect(url_for( 'weblogic.profile'))
    

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
    #db.create_all(app=app)
    app.register_blueprint(campaigns_api)
    app.register_blueprint(weblogic)
    app.register_blueprint(auth)
    app.run(port=7777, debug=True)
