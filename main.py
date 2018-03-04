from flask import Flask, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# temporary auth info, should be modeified
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '0000'

basic_auth = BasicAuth(app)

# Override Flask-admin's modelview to support basicauth
class ModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

# add Admin modelview
from models import User, Question, db ,Team
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(Team, db.session))

# Import the views module
from views import *


if __name__ == '__main__':
    db.app = app
    db.init_app(app)
    db.create_all()
    app.run()

