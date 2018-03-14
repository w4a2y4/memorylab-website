from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, default='')
    questions = db.relationship(
        'Question',
        backref='user',
        lazy='dynamic'
    )
    evolutions = db.relationship(
        'Evolution',
        backref='user',
        lazy='dynamic'
    )

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), default='')
    path = db.Column(db.Unicode(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, description='', path=''):
        self.description = description
        self.path = path

    def __repr__(self):
        return '<Question %r %r>' % ( self.description, self.path)


class Evolution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Unicode(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_question = db.Column(db.Integer)
    end_question= db.Column(db.Integer)

    def __init__(self, path='', start_question=0, end_question=0):
        self.path = path
        self.start_question = start_question
        self.end_question = end_question

    def __repr__(self):
        return '<Evolution %r %r>' % ( self.user_id, self.path)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), default='')
    picture_url = db.Column(db.String(200), default='')
    text = db.Column(db.String(200), default='')
    type_num=db.Column(db.Integer,default=0)

    def __init__(self, name='',picture_url='',text='',type_num=0):
        self.name=name
        self.picture_url=picture_url
        self.text=text
        self.type_num=type_num

    def __repr__(self):
        return '<Team %r %r %r %r>' % (self.name ,self.text,self.picture_url,self.type_num)
