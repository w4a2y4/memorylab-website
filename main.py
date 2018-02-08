from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# 設定資料庫位置，並建立 app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
