import os
import os.path as op
import random

from flask import Flask, Response, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin, BaseView, expose, form
from flask_admin.contrib.sqla import ModelView, filters
from flask_apscheduler import APScheduler  
from werkzeug.exceptions import HTTPException
from sqlalchemy.event import listens_for
from jinja2 import Markup

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# temporary auth info, should be modeified
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '0000'

basic_auth = BasicAuth(app)

# add Admin modelview
from models import db, User, Link, Question, Team, Evolution, TestUser, Settings, Huanan

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

evo_path = op.join(op.dirname(__file__), 'static/evolutions')
quest_path = op.join(op.dirname(__file__), 'static/questions')
prof_path = op.join(op.dirname(__file__), 'static/profile')
huanan_path = op.join(op.dirname(__file__), 'static/huanan')

try:
    os.mkdir(evo_path)
except OSError:
    pass
try:
    os.mkdir(quest_path)
except OSError:
    pass
try:
    os.mkdir(huanan_path)
except OSError:
    pass

@listens_for(Evolution, 'after_delete')
def del_evo(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(evo_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(evo_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass

@listens_for(Question, 'after_delete')
def del_quest(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(quest_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(quest_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass

@listens_for(User, 'after_delete')
def del_prof(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(prof_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(prof_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass

@listens_for(Huanan, 'after_delete')
def del_huanan(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(huanan_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(huanan_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass

# Override Flask-admin's modelview to support basicauth
class AdminView(ModelView):
    column_display_pk = True
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


class UserAdmin(AdminView):

    form_widget_args = {'description' : {'rows' : 10}}

    def _list_thumbnail(view, context, model, name):
        if not model.profile:
            return ''
        fname = 'profile/' + form.thumbgen_filename(model.profile)
        return Markup('<img src="%s">' % url_for('static',
                                                 filename=fname))
    column_formatters = {'profile': _list_thumbnail}
    form_extra_fields = {
        'profile': form.ImageUploadField('Evolution',
                                      base_path=prof_path,
                                      thumbnail_size=(100, 100, True))
    }


class EvolutionAdmin(AdminView):

    column_filters = ('user',)

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        fname = 'evolutions/' + form.thumbgen_filename(model.path)
        return Markup('<img src="%s">' % url_for('static',
                                                 filename=fname))
    column_formatters = {'path': _list_thumbnail}
    form_extra_fields = {
        'path': form.ImageUploadField('Evolution',
                                      base_path=evo_path,
                                      thumbnail_size=(100, 100, True))
    }


class QuestionAdmin(AdminView):

    column_filters = ('user',)

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        fname = 'questions/' + form.thumbgen_filename(model.path)
        return Markup('<img src="%s">' % url_for('static',
                                                 filename=fname))
    column_formatters = {'path': _list_thumbnail}
    form_extra_fields = {
        'path': form.ImageUploadField('Question',
                                      base_path=quest_path,
                                      thumbnail_size=(100, 100, True))
    }


class HuananAdmin(AdminView):

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        fname = 'huanan/' + form.thumbgen_filename(model.path)
        return Markup('<img src="%s">' % url_for('static',
                                                 filename=fname))
    column_formatters = {'path': _list_thumbnail}
    form_extra_fields = {
        'path': form.ImageUploadField('Huanan',
                                      base_path=huanan_path,
                                      thumbnail_size=(100, 100, True))
    }


admin = Admin(app, template_mode='bootstrap3')
admin.add_view(UserAdmin(User, db.session))
admin.add_view(AdminView(Link, db.session))
admin.add_view(QuestionAdmin(Question, db.session))
admin.add_view(EvolutionAdmin(Evolution, db.session))
admin.add_view(HuananAdmin(Huanan, db.session))
admin.add_view(AdminView(Team, db.session))
admin.add_view(AdminView(TestUser, db.session))
admin.add_view(AdminView(Settings, db.session))

# Import the views module
from views import *

db.app = app
db.init_app(app)
db.create_all()


from messenger_bot import send_message, send_image
import logging
import json
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

# Start at 12:30 
# @sched.scheduled_job('cron', hour='12', minute='30')
# Set all test user's question
def start_all_task():
    # log("====send all====")
    testUsers = TestUser.query.all()
    for u in testUsers:
        empty_questions = Question.query.filter_by(path='')
        e_question = empty_questions[random.randrange(0,empty_questions.count())]
        e_question.path = "Answering..."
        # text = e_question.description
        u.answering = e_question.id # Set the question testuser is answering
        db.session.commit()
        

# End at 24:30 (00:30)
# @sched.scheduled_job('cron', hour='00', minute='30')
def end_for_test():
    # log("====notice====")
    testUser = TestUser.query.all()
    for u in testUser:
        u.tested = False
        u.test_times += 1
        db.session.commit()

class Config(object):  
    JOBS = [{  
               'id':'job1',  
               'func':'main:start_all_task',  
               'args': '',  
               'trigger': {  
                    'type': 'cron',  
                    'hour':'00',  
                    'minute':'30',  
                }
            }, {  
               'id':'job3',  
               'func':'main:end_for_test',  
               'args': '',  
               'trigger': {  
                    'type': 'cron',  
                    'hour':'12',  
                    'minute':'44',    
                }
            }]  
    SCHEDULER_API_ENABLED = True

if __name__ == '__main__':
    scheduler = APScheduler()
    app.config.from_object(Config()) 
    scheduler.init_app(app)
    scheduler.start()
    app.run()


