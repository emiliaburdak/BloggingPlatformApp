from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comments', backref='user', passive_deletes=True)
    likes = db.relationship('Likes', backref='user', passive_deletes=True)
    saved = db.relationship('Post', secondary='saved', backref=db.backref('saved', lazy='dynamic'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    edit = db.Column(db.Boolean)
    comments = db.relationship('Comments', backref='post', passive_deletes=True)
    likes = db.relationship('Likes', backref='post', passive_deletes=True)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    edit_switch = db.Column(db.Boolean)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)


class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)


# tzw association table
class Saved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))