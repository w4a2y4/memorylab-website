from flask import render_template
from main import app
from models import User, Question, Team

# home page
@app.route('/')
def index():
    return render_template('index.html')


# flow
@app.route('/flow')
def flow():
    return render_template('flow.html')


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
    """
    boss=0 it=1 twoD=2 threeD=3 
    """
    teams = Team.query.all()
    boss = Team.query.filter_by(type_num = 0).all()
    it = Team.query.filter_by(type_num = 1).all()
    twoD = Team.query.filter_by(type_num = 2).all()
    threeD = Team.query.filter_by(type_num = 3).all()
    
    return render_template('team.html',teams=teams,boss=boss,it=it,twoD=twoD,threeD=threeD)
