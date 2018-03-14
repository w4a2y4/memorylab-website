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
@app.route('/character/<int:user_id>')
def character(user_id):

    user = User.query.get_or_404(user_id)
    name = user.name
    description = user.description
    profile = user.profile
    init = user.init.all()
    questions = user.questions.all()
    evolutions = user.evolutions.all()

    return render_template('character.html',
                           user=user,
                           name=name,
                           description=description,
                           profile=profile,
                           init=init,
                           questions=questions,
                           evolutions=evolutions)


# team
@app.route('/team')
def team():
    """
    boss=0 it=1 twoD=2 threeD=3 anim=4
    acent=5 ui=6 elect=7 out=8
    2D+3D=9 it+acent=10 ui+3D=11
    ui+2D=12 3D+accent=13
    """
    teams = Team.query.all()
    boss = Team.query.filter_by(type_num = 0).all()
    it = Team.query.filter((Team.type_num == 1) | (Team.type_num == 10)).all()
    twoD = Team.query.filter((Team.type_num == 2) | (Team.type_num ==9 ) | (Team.type_num == 12)).all()
    threeD = Team.query.filter((Team.type_num == 3) | (Team.type_num == 9) | (Team.type_num == 11) | (Team.type_num == 13)).all()
    anim = Team.query.filter_by(type_num = 4).all()
    acent = Team.query.filter((Team.type_num == 5) | (Team.type_num == 10) | (Team.type_num == 13)).all()
    ui = Team.query.filter((Team.type_num == 6) | (Team.type_num == 11) | (Team.type_num == 12)).all()
    elect = Team.query.filter_by(type_num = 7).all()
    out = Team.query.filter_by(type_num = 8).all()
    
    return render_template('team.html',teams=teams,boss=boss,it=it,twoD=twoD,threeD=threeD,anim=anim,acent=acent,ui=ui,elect=elect,out=out)
