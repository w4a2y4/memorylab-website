from flask import render_template
from main import app
from models import User, Question

# home page
@app.route('/')
def index():
    return render_template('index.html')


# the list of chracters
@app.route('/characters')
def characters():

    users = User.query.all()

    return render_template('characters.html',
                            users=users)


# each character
@app.route('/characters/<int:user_id>')
def character(user_id):

    user = User.query.get_or_404(user_id)
    name = user.name
    questions = user.questions.all()

    return render_template('character.html',
                           user=user,
                           name=name,
                           questions=questions)


# team
@app.route('/team')
def team():
    return render_template('team.html')