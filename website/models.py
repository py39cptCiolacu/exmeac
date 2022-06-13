from . import db

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    vote = db.Column(db.String(150))
    password = db.Column(db.String(150))
    time = db.Column(db.String(150))

    def __init__(self, vote= '0', password='NU', time='0'):
        self.vote = vote
        self.password = password
        self.time = time


class Motion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    motion = db.Column(db.String(1500))

    def __init__(self, motion):
        self.motion = motion
    

class Time(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.String(1500))

    def __init__(self, time):
        self.time = time


class Password(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(10))

    def __init__(self, password):
        self.password = password
