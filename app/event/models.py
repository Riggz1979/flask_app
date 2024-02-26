from sqlalchemy import UniqueConstraint

from app import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')
    begin_at = db.Column(db.Date, nullable=False)
    end_at = db.Column(db.Date, nullable=False)
    max_users = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)


class EventUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event')
    created_at = db.Column(db.Date, nullable=False)
    score = db.Column(db.Integer)
    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='_column1_column2_uc'),)
