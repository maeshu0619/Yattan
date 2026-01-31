from . import db
import datetime

class Feed(db.Model):
    __tablename__ = "feeds"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, default=lambda: datetime.date.today().isoformat())
    dog = db.Column(db.String)
    time = db.Column(db.String)
    fed = db.Column(db.Boolean, default=False)

class Walk(db.Model):
    __tablename__ = "walk"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, default=lambda: datetime.date.today().isoformat())
    taken = db.Column(db.Boolean, default=False)

class Trash(db.Model):
    __tablename__ = "trash"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, default=lambda: datetime.date.today().isoformat())
    taken = db.Column(db.Boolean, default=False)

class OptionalTask(db.Model):
    __tablename__ = "optional_tasks"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, default=lambda: datetime.date.today().isoformat())
    name = db.Column(db.String)
    done = db.Column(db.Boolean, default=False)
    count = db.Column(db.Integer, default=0)
