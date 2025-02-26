from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    credits = db.Column(db.Integer, default=0)

class Hunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    validation_method = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

class Clue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hunt_id = db.Column(db.Integer, db.ForeignKey('hunt.id'), nullable=False)
    clue_number = db.Column(db.Integer, nullable=False)
    photo_path = db.Column(db.String(200))
    clue_text = db.Column(db.String(500))
    gps_lat = db.Column(db.Float)
    gps_lon = db.Column(db.Float)

class LeaderboardEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hunt_id = db.Column(db.Integer, db.ForeignKey('hunt.id'), nullable=False)
    time_started = db.Column(db.DateTime, nullable=False)
    time_completed = db.Column(db.DateTime)
    attempts = db.Column(db.Integer, default=0)
