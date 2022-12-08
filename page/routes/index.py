from flask import Blueprint, render_template

index = Blueprint("index", __name__)


@index.route("/", methods=["GET"])
def get_index():
    return render_template("index.html")
