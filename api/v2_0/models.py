from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Table, inspect, select
from sqlalchemy.orm import relationship, Session
from flask_login import UserMixin

dbsql = SQLAlchemy()


def to_dict(table: Table):
    """to_dict can convert any SQLAlchemy ORM Table to a Python dict.
    Args:
        table (Table): Any SQLAlchemy ORM Table.
    """
    ### Comments reference the line below the comment, not the one above.
    returned_dict = {}
    # Gets all the different column names from the given table
    table_columns = [table_column.name for table_column in inspect(table).c]
    # Gets all the entries in the table
    table_rows = table.query.all()
    for row in table_rows:
        # Save the id (primary key) of the current entry
        row_id = row.id
        # Convert the row (Type: Table( to a dict, so that we can work with it easier
        row = row.__dict__
        # A temporary dictionary for the specific entry we are working on
        row_dict = {}
        for column in table_columns:
            # add all the column names and their respective values into the temporary dictionary
            row_dict[str(column)] = row[column]
        # Save the temporary dictionary to the main dictionary
        returned_dict[row_id] = row_dict
    return returned_dict


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
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    email = dbsql.Column(dbsql.String(100), unique=True)
    password = dbsql.Column(dbsql.String(100))
    name = dbsql.Column(dbsql.String(1000))
    email_confirm = dbsql.Column(dbsql.Boolean)
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


class Campaign(dbsql.Model):
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


class Devices(dbsql.Model):
    __tablename__ = "devices"
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    key = dbsql.Column(dbsql.String)
    name = dbsql.Column(dbsql.String)