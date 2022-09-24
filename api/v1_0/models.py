from db import dbsql as db
from flask_login import login_manager, UserMixin

ACCESS = {
    'guest': 0,
    'user': 1,
    'DM': 2,
    'admin' : 3
}

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    email_confirm = db.Column(db.Boolean)
    access = db.Column(db.Integer)
    #dm_of
    #player_in
    def is_admin(self):
        return self.access == ACCESS['admin']
 
    def is_dm(self):
        return self.access >= ACCESS['DM']

    def is_user(self):
        return self.access >= ACCESS['user']

    def is_guest(self):
        return self.access == ACCESS['guest']

class MentorProgramm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentorId = db.Column(db.Integer)
    studentId = db.Column(db.Integer)
    format = db.Column(db.String)
    ruleset = db.Column(db.String)
    description = db.Column(db.String)
    language = db.Column(db.String)

class Ruleset(db.Model):
    ruleset = db.Column(db.String, primary_key=True)



          
