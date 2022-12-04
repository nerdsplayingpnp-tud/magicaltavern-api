import sqlalchemy

from sqlalchemy_serializer import SerializerMixin
from flask import abort, request
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


def ensure_player_exists(user_id: int):
    """If a player (User) doesn't exist, a new user with the supplied id will get created and returned. If the user already exists, that user gets returned.

    Args:
        user_id (int): The user id to ensure.

    Returns:
        _type_: A User object
    """
    user_exists = User.query.filter(User.id == user_id).one_or_none()
    if not user_exists:
        new_user = User(id=user_id, access=1)
        dbsql.session.add(new_user)
        dbsql.session.commit()
        return new_user
    return user_exists


def does_campaign_exist(request: request, campaign_id: int):
    campaign = Campaign.query.filter(Campaign.id == campaign_id).one_or_none()
    if not campaign:
        abort(400, "This Campaign does not exist.")
    return campaign


def campaign_not_finished(request: request, campaign_id: int):
    campaign = does_campaign_exist(request, campaign_id)
    if campaign.finished:
        abort(409, "The campaign is finished. Modifications are not allowed.")
    return


def campaign_cannot_be_active(request: request, campaign_id: int):
    campaign = does_campaign_exist(request, campaign_id)
    if campaign.active:
        abort(409, "The campaign is not active. Player modifications are not allowed.")
    return


ACCESS = {"guest": 0, "user": 1, "DM": 2, "admin": 3}
COMPLEXITY = {"easy": 0, "medium": 1, "hard": 2}
LENGTH = {"short": 0, "medium": 1, "long": 2}
LANGUAGE = {"eng": 0, "ger": 1, "gereng": 2}


campaign_player_association = Table(
    "campaign_player_association",
    dbsql.metadata,
    Column("player", ForeignKey("user.id"), primary_key=True),
    Column("campaign", ForeignKey("campaign.id"), primary_key=True),
)

campaign_dm_association = Table(
    "campaign_dm_association",
    dbsql.metadata,
    Column("dm", ForeignKey("user.id"), primary_key=True),
    Column("campaign", ForeignKey("campaign.id"), primary_key=True),
)


class User(UserMixin, dbsql.Model, SerializerMixin):
    __tablename__ = "user"
    serialize_rules = ("-player_in", "-dm_of")
    id = dbsql.Column(dbsql.Integer, primary_key=True, unique=True)
    name = dbsql.Column(dbsql.String(1000))
    access = dbsql.Column(dbsql.Integer)
    player_in = relationship(
        "Campaign", secondary=campaign_player_association, back_populates="players"
    )
    dm_of = relationship(
        "Campaign", secondary=campaign_dm_association, back_populates="dm"
    )

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


# Ruleset class does not get used for now. Do not delete though, in case we want to work with it in the future.
class Ruleset(dbsql.Model, SerializerMixin):
    __tablename__ = "ruleset"
    serialize_rules = ("-used_by",)
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    ruleset = dbsql.Column(dbsql.String)
    used_by = relationship("Campaign")


class Campaign(dbsql.Model, SerializerMixin):
    __tablename__ = "campaign"
    serialize_rules = ("-players", "-dm")
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    name = dbsql.Column(
        dbsql.String,
    )
    description = dbsql.Column(dbsql.String, nullable=False)
    dm = relationship("User", secondary=campaign_dm_association, back_populates="dm_of")
    players_min = dbsql.Column(dbsql.Integer, nullable=False)
    players_max = dbsql.Column(dbsql.Integer, nullable=False)
    players = relationship(
        "User", secondary=campaign_player_association, back_populates="player_in"
    )
    complexity = dbsql.Column(dbsql.Integer, nullable=False)
    place = dbsql.Column(dbsql.Integer, nullable=False)
    time = dbsql.Column(dbsql.String, nullable=False)
    content_warnings = dbsql.Column(dbsql.String, nullable=False)
    complexity = dbsql.Column(dbsql.Integer, nullable=False)
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
