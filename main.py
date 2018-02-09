from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

from models import User, Question

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Question, db.session))

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()