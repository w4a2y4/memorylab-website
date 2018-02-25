from flask import render_template
from main import app
from models import User, Question

# home page
@app.route('/')
def index():
    return render_template('index.html')

# the list of chracter
@app.route('/characters')
def characters():
    return render_template('characters.html',Users = User.query.all())

# each character
@app.route('/characters/<userid>')
def character(userid):
    return render_template('character.html',Users = User.query.all(), Quess=Question.query.all(), userid=userid )

# team
@app.route('/team')
def others():
    return render_template('team.html')