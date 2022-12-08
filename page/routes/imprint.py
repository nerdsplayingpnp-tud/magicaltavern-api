from flask import Blueprint, render_template

imprint = Blueprint("imprint", __name__)


@imprint.route("/impressum", methods=["GET"])
def impressum_page():
    return render_template("impressum.html")
