from flask import Blueprint, render_template
from flask_login import current_user
from db import dbsql as db
from api.v2_0.models import MentorProgramm, Ruleset

mentor = Blueprint("mentor", __name__)


@mentor.route("/mentor", methods=["GET"])
def mentor_page():
    rulesets = Ruleset.query.all()
    if not rulesets:
        ruleset = Ruleset(ruleset="DnD 5th Edition")
        db.session.add(ruleset)
        db.session.commit()
    programms = MentorProgramm.query.all()
    openProgramms = []
    mentoredProgramms = []
    if current_user.is_authenticated:
        for programm in programms:
            if not programm.mentorId:
                openProgramms.append(programm)
            if programm.mentorId == current_user.id:
                mentoredProgramms.append(programm)
    return render_template(
        "dm_Mentor.html",
        rulesets=rulesets,
        openProgramms=openProgramms,
        mentoredProgramms=mentoredProgramms,
    )
