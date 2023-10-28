# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Bailey Roberts - Youssef Alaoui - Aydan Guliyeva


from datetime import datetime

from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from flask_app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"{self.id} {self.firstname} {self.lastname}  {self.dob} {self.email} {self.password}"


class Profile(db.Model):
    __tablename__ = 'profile'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    photo = db.Column(db.Text)
    bio = db.Column(db.Text)
    gender = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('user', uselist=False))
    posts = db.relationship('Posts', back_populates="author")
    comments = db.relationship('Comments', back_populates="comment_author")
    like = db.relationship('Likes', back_populates="profile_liked")
    comment_like = db.relationship('Comment_Likes', back_populates='profile_liked')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Posts(db.Model):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    title = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    author = db.relationship("Profile", back_populates='posts')
    comment = db.relationship('Comments', back_populates='post_commented')
    like = db.relationship('Likes', back_populates='post_liked')
    comment_like = db.relationship('Comment_Likes', back_populates='post_comment_liked')

    def __repr__(self):
        return '<Posts {}>'.format(self.body)


class Comments(db.Model):
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    comment_author = db.relationship("Profile", back_populates='comments')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post_commented = db.relationship('Posts', back_populates='comment')
    like = db.relationship('Comment_Likes', back_populates='comment_liked')


class Likes(db.Model):
    __tablename__ = 'likes'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    profile_liked = db.relationship("Profile", back_populates='like')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post_liked = db.relationship('Posts', back_populates='like')


class Comment_Likes(db.Model):
    __tablename__ = 'comment_likes'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    profile_liked = db.relationship("Profile", back_populates='comment_like')
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    comment_liked = db.relationship('Comments', back_populates='like')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post_comment_liked = db.relationship('Posts', back_populates='comment_like')
