import sqlalchemy

from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Table, inspect
from sqlalchemy.orm import relationship

from flask_login import UserMixin

dbsql = SQLAlchemy()


def table_to_dict(model: dbsql.Model) -> dict:
    """table_to_dict can convert any SQLAlchemy ORM Table with one primary key to a Python dict.
    Args:
        model (SQLAlchemy.Model): Any SQLAlchemy ORM Table.
    """
    returned_dict = {}
    primary_key = str(inspect(model).primary_key[0].name)
    entries = model.query.all()
    for entry in entries:
        returned_dict[getattr(entry, primary_key)] = entry.to_dict()
    return returned_dict


def ensure_player_exists(user_id: int) -> None:
    if User.query.filter(User.id == user_id).one_or_none() == None:
        new_user = User(id=user_id, access=1)
        dbsql.session.add(new_user)
        dbsql.session.commit()
        return
    return


ACCESS = {"guest": 0, "user": 1, "DM": 2, "admin": 3}
COMPLEXITY = {"easy": 0, "medium": 1, "hard": 2}
LENGTH = {"short": 0, "medium": 1, "long": 2}
LANGUAGE = {"eng": 0, "ger": 1, "gereng": 2}

campaign_player_association = Table(
    "campaign_player_association",
    dbsql.metadata,
    Column("player", ForeignKey("user.id")),
    Column("campaign", ForeignKey("campaign.id")),
)

campaign_dm_association = Table(
    "campaign_dm_association",
    dbsql.metadata,
    Column("dm", ForeignKey("user.id")),
    Column("campaign", ForeignKey("campaign.id")),
)


class User(UserMixin, dbsql.Model):
    __tablename__ = "user"
    id = dbsql.Column(dbsql.Integer, primary_key=True, unique=True)
    name = dbsql.Column(dbsql.String(1000))
    access = dbsql.Column(dbsql.Integer)
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


class MentorProgramm(dbsql.Model):
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    mentorId = dbsql.Column(dbsql.Integer)
    studentId = dbsql.Column(dbsql.Integer)
    format = dbsql.Column(dbsql.String)
    ruleset = dbsql.Column(dbsql.String)
    description = dbsql.Column(dbsql.String)
    language = dbsql.Column(dbsql.String)


class Ruleset(dbsql.Model):
    __tablename__ = "ruleset"
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    ruleset = dbsql.Column(dbsql.String)
    used_by = relationship("Campaign")


class Campaign(dbsql.Model, SerializerMixin):
    __tablename__ = "campaign"
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    name = dbsql.Column(
        dbsql.String,
    )
    description = dbsql.Column(dbsql.String, nullable=False)
    players_min = dbsql.Column(dbsql.Integer, nullable=False)
    players_max = dbsql.Column(dbsql.Integer, nullable=False)
    players_current = dbsql.Column(dbsql.Integer)
    complexity = dbsql.Column(dbsql.Integer, nullable=False)
    place = dbsql.Column(dbsql.Integer, nullable=False)
    time = dbsql.Column(dbsql.String, nullable=False)
    content_warnings = dbsql.Column(dbsql.String, nullable=False)
    ruleset = dbsql.Column(dbsql.Integer, ForeignKey("ruleset.id"), nullable=False)
    campaign_length = dbsql.Column(dbsql.Integer, nullable=False)
    language = dbsql.Column(dbsql.Integer, nullable=False)
    character_creation = dbsql.Column(dbsql.String, nullable=False)
    briefing = dbsql.Column(dbsql.String, nullable=False)
    notes = dbsql.Column(dbsql.String, nullable=False)
    image_url = dbsql.Column(dbsql.String)
    message_id = dbsql.Column(dbsql.Integer, unique=True)
    active = dbsql.Column(dbsql.Boolean, default=False, nullable=False)
    finished = dbsql.Column(dbsql.Boolean, default=False, nullable=False)


class Devices(dbsql.Model):
    __tablename__ = "devices"
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    key = dbsql.Column(dbsql.String)
    name = dbsql.Column(dbsql.String)
