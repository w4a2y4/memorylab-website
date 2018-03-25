from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

import random
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, default='')
    profile = db.Column(db.Unicode(128))
    description = db.Column(db.Text, default='')
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
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, default='')
    path = db.Column(db.Unicode(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    test_answer = db.relationship("TestAnswer", backref="question")
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

    def __len__(self):
        return len(self.coordinate_row)


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

class TestUser(db.Model):
    __tablename__ = 'testuser'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default='')
    fb_id = db.Column(db.String(50), unique=True)
    tested = db.Column(db.Boolean, default=False)
    sequence = db.Column(db.String(1024), default='')
    test_times = db.Column(db.Integer, default = 0)
    test_answer = db.relationship("TestAnswer", backref="testuser")
    def __init__(self, name = '', fb_id=''):
        self.name = name
        self.fb_id = fb_id
        id_list = [i[0] for i in db.session.query(User.id).distinct()]
        random.shuffle(id_list)
        self.sequence = json.dumps(id_list)
    def __repr__(self):
        return '<TestUser %r>' % self.fb_id

class TestAnswer(db.Model):
    __tablename__ = 'testanswer'
    id = db.Column(db.Integer, primary_key=True)
    test_user_id = db.Column(db.Integer, db.ForeignKey('testuser.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    path = db.Column(db.Unicode(128))
    def __init__(self, path=''):
        self.path=path
    def __repr__(self):
        return '<TestAnswer %r %r >' % (self.question_id ,self.test_user_id)
