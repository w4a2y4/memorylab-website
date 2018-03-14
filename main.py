import os
import os.path as op

from flask import Flask, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin, BaseView, expose, form
from flask_admin.contrib.sqla import ModelView
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
from models import db, User, Question, Team, Evolution

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

file_path = op.join(op.dirname(__file__), 'static/files')
try:
    os.mkdir(file_path)
except OSError:
    pass

@listens_for(Evolution, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass

class EvolutionView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        fname = 'files/' + form.thumbgen_filename(model.path)
        return Markup('<img src="%s">' % url_for('static',
                                                 filename=fname))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Evolution',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }

# Override Flask-admin's modelview to support basicauth
class ModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(EvolutionView(Evolution, db.session))
admin.add_view(ModelView(Team, db.session))

# Import the views module
from views import *

if __name__ == '__main__':
    db.app = app
    db.init_app(app)
    db.create_all()
    app.run()

