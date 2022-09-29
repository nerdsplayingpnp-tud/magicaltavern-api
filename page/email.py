from wsgiref.util import request_uri
from werkzeug.security import generate_password_hash, check_password_hash
from flask import *
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    login_required,
    logout_user,
)
from flask_mail import Mail, Message
from handle_apikeys import generate, put
from pathlib import Path
from api.v2_0.models import dbsql as db
import json, time
from api.v1_0.campaigns import get_campaigns, db_campaigns, toggle_player_web
from main import mail
from api.v2_0.models import User, MentorProgramm, Ruleset
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature


email = Blueprint("email", __name__)
# collecting all the salts for the tokens for email authentication
# email-confirm: 9XQynYwmt5kVo5Tc1GpEo9tynRWrgT
# camp-confirm: 6iyEu3rd2O8ihz8LASX101AQBfGS8p
# password reset: iL0dtRvkF5f5ekUy7NBLe2OJH44qfI
# Free Salt for Whenever: ltDySgN8aeLfzGSiHitY09sFZWQTo9


# ---------------------------------------------------------------------------------------
# functions to confirm email Tokens and following actions
# ---------------------------------------------------------------------------------------


# verify the changeEmail-Profile action
# Check if user password hash is the right salt, to see if the ID has been tempered with
@email.route("/confirm_new_Email/<token>/<id>", methods=["GET"])
def confirm_new_Email(token, id):
    user = User.query.filter_by(id=id).first()

    try:
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=user.password)
        email = s.loads(token, salt=user.password, max_age=3600)
    except (SignatureExpired, BadSignature):
        return render_template("error.html")
    user.email = email
    db.session.commit()
    flash("Your Email has been changed!")
    return redirect(url_for("weblogic.profile"))


# signup Email verification
@email.route("/confirm_email/<token>", methods=["GET"])
def confirm_Email(token):
    # verify token
    try:
        s = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"], salt="9XQynYwmt5kVo5Tc1GpEo9tynRWrgT"
        )
        email = s.loads(token, salt="9XQynYwmt5kVo5Tc1GpEo9tynRWrgT", max_age=3600)
    except (SignatureExpired, BadSignature):
        return render_template("error.html")
    user = User.query.filter_by(email=email).first()
    user.email_confirm = True
    db.session.commit()
    flash("Your Email has been confirmed!")
    return redirect(url_for("auth.login"))


# Campaign signup without login
@email.route("/confirm_email_campaign/<token>/<key>", methods=["GET"])
def confirm_Email_campaign(token, key):
    # verify token
    try:
        s = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"], salt="6iyEu3rd2O8ihz8LASX101AQBfGS8p"
        )
        email = s.loads(token, salt="6iyEu3rd2O8ihz8LASX101AQBfGS8p", max_age=3600)
    except (SignatureExpired, BadSignature):
        return render_template("error.html")
    user = User.query.filter_by(email=email).first()
    if not user.email_confirm:
        user.email_confirm = True
        db.session.commit()
    login_user(user)
    toggle_player_web(key)
    logout_user()
    flash("You have been signed up!")
    return redirect(url_for("weblogic.campaign_page"))


# Reset Password verification
@email.route("/reset_password/<token>", methods=["GET", "POST"])
def resetPassword(token):
    if request.method == "GET":
        # verify token
        try:
            s = URLSafeTimedSerializer(
                current_app.config["SECRET_KEY"], salt="iL0dtRvkF5f5ekUy7NBLe2OJH44qfI"
            )
            email = s.loads(token, salt="iL0dtRvkF5f5ekUy7NBLe2OJH44qfI", max_age=3600)
        except (SignatureExpired, BadSignature):
            return render_template("error.html")
        user = User.query.filter_by(email=email).first()
        return render_template("reset_password.html", token=token)
    if request.method == "POST":
        password = request.form.get("password")
        passwordConfirm = request.form.get("passwordConfirm")
        try:
            s = URLSafeTimedSerializer(
                current_app.config["SECRET_KEY"], salt="iL0dtRvkF5f5ekUy7NBLe2OJH44qfI"
            )
            email = s.loads(token, salt="iL0dtRvkF5f5ekUy7NBLe2OJH44qfI", max_age=3600)
        except (SignatureExpired, BadSignature):
            return render_template("error.html")
        if password == passwordConfirm:
            user = User.query.filter_by(email=email).first()
            user.password = generate_password_hash(password, method="sha256")
            db.session.commit()
        else:
            flash("Passwords werent the same!")
            return redirect("/reset_password/" + token)
        flash("New Password has been set")
        return redirect(url_for("auth.login"))


# ---------------------------------------------------------------------------------------
# functions to send mails
# ---------------------------------------------------------------------------------------
# @app.route('/validate', methods=["POST"])
# no reason right now for this to be callable from outside
# function sends email for Account sign up authentication with appropriate salt and token
def validate(email):
    s = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"], salt="9XQynYwmt5kVo5Tc1GpEo9tynRWrgT"
    )
    token = s.dumps(email, salt="9XQynYwmt5kVo5Tc1GpEo9tynRWrgT")
    msg = Message(
        "PnP Email Authentication",
        sender=("Nerds Play PnP", "nerdsplaypnpvalidator@gmail.com"),
        recipients=[email],
    )
    msg.body = (
        "Hello Adventurer, to complete the signup you have to confirm your email. Click the link to confirm your Email: "
        + request.url_root
        + url_for("email.confirm_Email", token=token)
    )
    mail.send(msg)
    return None


# Profile Change Email Action
# Use User password hash as Salt to not allow changing of Id to change email of another account (Name, Id or Email is not safe as Name is not unique and can be prepared for attack, Id is too simple and email can be publicly known )
def validateNewEmail(email, id, hash):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=hash)
    token = s.dumps(email, salt=hash)
    msg = Message(
        "PnP Email Authentication",
        sender=("Nerds Play PnP", "nerdsplaypnpvalidator@gmail.com"),
        recipients=[email],
    )
    msg.body = (
        "Hello Adventurer, to change your Email you have to confirm your new Email. Click the link to confirm your Email: "
        + request.url_root
        + url_for("email.confirm_new_Email", token=token, id=id)
    )
    mail.send(msg)
    return None


# Signup for Campaign without account Email
def validateCampaign(email, key):
    s = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"], salt="6iyEu3rd2O8ihz8LASX101AQBfGS8p"
    )
    token = s.dumps(email, salt="6iyEu3rd2O8ihz8LASX101AQBfGS8p")
    msg = Message(
        "PnP Email Authentication",
        sender=("Nerds Play PnP", "nerdsplaypnpvalidator@gmail.com"),
        recipients=[email],
    )
    msg.body = (
        "Hello Adventurer, ready for your next Adventure? Click the link to confirm your Email: "
        + request.url_root
        + url_for("email.confirm_Email_campaign", token=token, key=key)
    )
    mail.send(msg)
    return None


# ---------------------------------------------------------------------------------------
# Campaign Sign up
# ---------------------------------------------------------------------------------------

# Signup for Campaign with account
@email.route("/signUpCampaign/<key>", methods=["POST"])
@login_required
def signUpCampaign(key):
    toggle_player_web(key)
    flash("You have been signed up for this campaign")
    return redirect(url_for("weblogic.campaign_page"))


# Signup for Campaign without account
@email.route("/signUpCampaignEmail/<key>", methods=["POST"])
def signUpCampaignEmail(key):
    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    if user:
        if user.is_guest():
            validateCampaign(email, key)
            flash("You need to confirm your Email Address, check your inbox")
            return redirect(url_for("weblogic.campaign_page"))
        else:
            flash("Error account with email exists, please sign in")
            return redirect(url_for("auth.login"))
    else:
        new_guest = User(
            email=email,
            name="guest",
            password=generate_password_hash("password", method="sha256"),
            email_confirm=False,
            access=0,
        )
        # new_guest.name = "guest" + new_guest.id
        db.session.add(new_guest)
        db.session.commit()
        validateCampaign(email, key)
        flash("You need to confirm your Email Address, check your inbox")
        return redirect(url_for("weblogic.campaign_page"))


# Signup for Campaign without account
@email.route("/sendMailtoPlayers/<key>", methods=["POST"])
@login_required
def sendMailtoPlayers(key):
    if not current_user.is_dm():
        flash("Only Dungeonmasters have authority for this command")
        return redirect(url_for("auth.login"))
    text = request.form.get("text")
    campaigns_json = get_campaigns()[0].json
    campaign = campaigns_json[key]
    msg = Message(
        "Mail to all Players in " + campaign["name"],
        sender=(
            current_user.name + ", Gamemaster of " + campaign["name"],
            "nerdsplaypnpvalidator@gmail.com",
        ),
        recipients=campaign["players"],
    )
    msg.body = text
    mail.send(msg)
    flash("The Email has been sent to your players")
    return redirect(url_for("weblogic.DmPage"))


# ---------------------------------------------------------------------------------------
# Signup actions
# ---------------------------------------------------------------------------------------
# Logic for Reset/Forgot Password
@email.route("/reset_password", methods=["POST", "GET"])
def reset_password_mail():
    if request.method == "GET":
        return render_template("reset_password_mail.html")
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email is not registered")
            return redirect(url_for("auth.login"))
        s = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"], salt="iL0dtRvkF5f5ekUy7NBLe2OJH44qfI"
        )
        token = s.dumps(email, salt="iL0dtRvkF5f5ekUy7NBLe2OJH44qfI")
        msg = Message(
            "PnP Reset Password",
            sender=("Nerds Play PnP", "nerdsplaypnpvalidator@gmail.com"),
            recipients=[email],
        )
        msg.body = (
            "Hello Adventurer, click the link to reset your password:"
            + request.url_root
            + url_for("email.resetPassword", token=token)
        )
        mail.send(msg)
        flash("Please check your Inbox")
        return redirect(url_for("auth.login"))


# ---------------------------------------------------------------------------------------
# Profile actions
# ---------------------------------------------------------------------------------------
@email.route("/changeName", methods=["GET", "POST"])
@login_required
def change_Name():
    if request.method == "GET":
        return render_template("profile.html", user=current_user, changeName=True)
    if request.method == "POST":
        name = request.form.get("newName")
        user = User.query.filter_by(id=current_user.id).first()
        user.name = name
        db.session.commit()
        flash("New Name has been set!")
        return redirect(url_for("weblogic.profile"))


# Use Salt of User name to not allow changing of Id to change email of another account
@email.route("/changePassword", methods=["GET", "POST"])
@login_required
def change_Password():
    if request.method == "GET":
        return render_template("profile.html", user=current_user, changePassword=True)
    if request.method == "POST":
        oldPass = request.form.get("oldPassword")
        newPass = request.form.get("newPassword")
        user = User.query.filter_by(id=current_user.id).first()
        if not check_password_hash(user.password, oldPass):
            flash("wrong password")
            return redirect(url_for("weblogic.profile"))
        user.password = generate_password_hash(newPass, method="sha256")
        db.session.commit()
        flash("New Password has been set!")
        return redirect(url_for("weblogic.profile"))


@email.route("/changeEmail", methods=["GET", "POST"])
@login_required
def change_Email():
    if request.method == "GET":
        return render_template("profile.html", user=current_user, changeEmail=True)
    if request.method == "POST":
        email = request.form.get("email")
        validateNewEmail(email, current_user.id, current_user.password)
        flash("Please check your Inbox to confirm your new Email.")
        return redirect(url_for("weblogic.profile"))


@email.route("/deleteAccount", methods=["GET", "POST"])
@login_required
def deleteAccount():
    if request.method == "GET":
        return render_template("profile.html", user=current_user, deleteAccount=True)
    if request.method == "POST":
        password = request.form.get("password")
        user = User.query.filter_by(id=current_user.id).first()
        if not check_password_hash(user.password, password):
            flash("wrong password")
            return redirect(url_for("weblogic.profile"))
        logout_user()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("weblogic.index"))


# ---------------------------------------------------------------------------------------
# Admin actions
# ---------------------------------------------------------------------------------------
@email.route("/makeUser/<id>", methods=["POST"])
@login_required
def makeUser(id):
    if not current_user.is_admin():
        flash("You dont have a level 9 Wish..  Only Admins have access to this command")
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(id=id).first()
    user.access = 1
    db.session.commit()
    return redirect(url_for("weblogic.AdminPage"))


@email.route("/makeDM/<id>", methods=["POST"])
@login_required
def makeDM(id):
    if not current_user.is_admin():
        flash("You dont have a level 9 Wish..  Only Admins have access to this command")
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(id=id).first()
    user.access = 2
    db.session.commit()
    return redirect(url_for("weblogic.AdminPage"))


@email.route("/makeAdmin/<id>", methods=["POST"])
@login_required
def makeAdmin(id):
    if not current_user.is_admin():
        flash("You dont have a level 9 Wish..  Only Admins have access to this command")
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(id=id).first()
    user.access = 3
    db.session.commit()
    return redirect(url_for("weblogic.AdminPage"))


# ---------------------------------------------------------------------------------------
# Mentor-Page Actions
# ---------------------------------------------------------------------------------------
@email.route("/mentorPlayer", methods=["POST"])
@login_required
def mentorPlayer():
    ruleset = request.form.get("ruleset")
    format = request.form.get("format")
    description = request.form.get("description")
    language = request.form.get("language")
    mentor = MentorProgramm(
        studentId=current_user.id,
        format=format,
        ruleset=ruleset,
        description=description,
        language=language,
    )
    db.session.add(mentor)
    db.session.commit()
    return redirect(url_for("weblogic.mentor_page"))


@email.route("/takeOnTrainee/<programmId>", methods=["POST"])
@login_required
def takeOnTrainee(programmId):
    if not current_user.is_dm():
        flash("You dont have the rights")
        return redirect(url_for("weblogic.index"))
    programm = MentorProgramm.query.filter_by(id=programmId).first()
    programm.mentorId = current_user.id
    db.session.commit()
    return redirect(url_for("weblogic.mentor_page"))


@email.route("/leaveTrainee/<programmId>", methods=["POST"])
@login_required
def leaveTrainee(programmId):
    if not current_user.is_dm():
        flash("You dont have the rights")
        return redirect(url_for("weblogic.index"))
    programm = MentorProgramm.query.filter_by(id=programmId).first()
    programm.mentorId = None
    db.session.commit()
    return redirect(url_for("weblogic.mentor_page"))


@email.route("/newRuleset", methods=["post"])
def newRuleset():
    ruleset = request.form.get("ruleset")
    ruleset = Ruleset(ruleset=ruleset)
    db.session.add(ruleset)
    db.session.commit()
    return redirect(url_for("weblogic.mentor_page"))
