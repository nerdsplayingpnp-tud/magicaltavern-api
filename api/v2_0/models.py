from db import dbsql as db
from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import relationship
from flask_login import UserMixin


ACCESS = {"guest": 0, "user": 1, "DM": 2, "admin": 3}
COMPLEXITY = {"easy": 0, "medium": 1, "hard": 2}
LENGTH = {"short": 0, "medium": 1, "long": 2}
LANGUAGE = {"eng": 0, "ger": 1, "gereng": 2}

campaign_player_association = Table(
    "campaign_player_association",
    db.metadata,
    Column("player", ForeignKey("user.id")),
    Column("campaign", ForeignKey("campaign.id")),
)

campaign_dm_association = Table(
    "campaign_dm_association",
    db.metadata,
    Column("dm", ForeignKey("user.id")),
    Column("campaign", ForeignKey("campaign.id")),
)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    email_confirm = db.Column(db.Boolean)
    access = db.Column(db.Integer)
    player_in = relationship("Campaign", secondary=campaign_player_association)
    dm_of = relationship("Campaign", secondary=campaign_dm_association)

    def is_admin(self):
        return self.access == ACCESS["admin"]

    def is_dm(self):
        return self.access >= ACCESS["DM"]

    def is_user(self):
        return self.access >= ACCESS["user"]

    def is_guest(self):
        return self.access == ACCESS["guest"]


class MentorProgramm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentorId = db.Column(db.Integer)
    studentId = db.Column(db.Integer)
    format = db.Column(db.String)
    ruleset = db.Column(db.String)
    description = db.Column(db.String)
    language = db.Column(db.String)


class Ruleset(db.Model):
    __tablename__ = "ruleset"
    id = db.Column(db.Integer, primary_key=True)
    ruleset = db.Column(db.String)
    used_by = relationship("Campaign")


class Campaign(db.Model):
    __tablename__ = "campaign"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String,
    )
    description = db.Column(db.String, nullable=False)
    players_min = db.Column(db.Integer, nullable=False)
    players_max = db.Column(db.Integer, nullable=False)
    players_current = db.Column(db.Integer)
    complexity = db.Column(db.Integer, nullable=False)
    place = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String, nullable=False)
    content_warnings = db.Column(db.String, nullable=False)
    ruleset = db.Column(db.Integer, ForeignKey("ruleset.id"), nullable=False)
    campaign_length = db.Column(db.Integer, nullable=False)
    language = db.Column(db.Integer, nullable=False)
    character_creation = db.Column(db.String, nullable=False)
    briefing = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
