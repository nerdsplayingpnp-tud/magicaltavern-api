from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required
from api.v2_0.models import User

admin_page = Blueprint("admin_page", __name__)


@admin_page.route("/AdminPage")
@login_required
def AdminPage():
    if not current_user.is_admin():
        return redirect(url_for("weblogic.index"))
    users = User.query.all()
    return render_template("AdminPage.html", users=users)
