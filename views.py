from flask import render_template, redirect, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug import secure_filename
from main import app
from models import db, User, Link, Question, Team, TestUser, Settings, Huanan
import urllib.request
import json

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/questions'
configure_uploads(app, photos)

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
    settings = Settings.query.get_or_404(1)

    return render_template('characters.html',
                           users=users,
                           settings=settings)


# each character
@app.route('/character/<int:user_id>')
def character(user_id):

    user = User.query.get_or_404(user_id)
    name = user.name
    description = user.description
    profile = user.profile
    links = user.links.all()
    questions = user.questions.filter(Question.path != '')
    evolutions = user.evolutions.all()
    settings = Settings.query.get_or_404(1)

    return render_template('character.html',
                           user=user,
                           name=name,
                           description=description,
                           profile=profile,
                           links=links,
                           questions=questions,
                           evolutions=evolutions,
                           settings=settings)


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
    boss = Team.query.filter_by(type_num=0).all()
    it = Team.query.filter((Team.type_num == 1) | (Team.type_num == 10)).all()
    twoD = Team.query.filter((Team.type_num == 2) | (
        Team.type_num == 9) | (Team.type_num == 12)).all()
    threeD = Team.query.filter((Team.type_num == 3) | (Team.type_num == 9) | (
        Team.type_num == 11) | (Team.type_num == 13)).all()
    anim = Team.query.filter_by(type_num=4).all()
    acent = Team.query.filter((Team.type_num == 5) | (
        Team.type_num == 10) | (Team.type_num == 13)).all()
    ui = Team.query.filter((Team.type_num == 6) | (
        Team.type_num == 11) | (Team.type_num == 12)).all()
    elect = Team.query.filter_by(type_num=7).all()
    out = Team.query.filter_by(type_num=8).all()

    return render_template('team.html', teams=teams, boss=boss, it=it, twoD=twoD, threeD=threeD, anim=anim, acent=acent, ui=ui, elect=elect, out=out)


# HuaNan daddy
@app.route('/huanan')
def huanan():

    pics = Huanan.query.all()
    return render_template('huanan.html', pics=pics)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/answer/<id>', methods=['GET', 'POST'])
def answer(id):
    if request.method == 'POST' and 'photo' in request.files:
        u = TestUser.query.filter_by(fb_id=id).first()
        filename = photos.save(request.files['photo'])
        u.tested = True

        q = Question.query.filter_by(
	                                id=u.answering).first()
        q.path = filename
        db.session.commit()
        return redirect(request.base_url + "?upload")
    if request.method == 'GET':
        u = TestUser.query.filter_by(fb_id=id).first()
        seq = json.loads(u.sequence)
        user = User.query.get(seq[u.test_times])
        q_filter = Question.query.filter(
            Question.user == user, Question.path != '').order_by("id desc").limit(5).all()
        questions = list(q_filter)
        question = Question.query.get_or_404(u.answering).description
        opt_param = request.args.get("upload")
        upload = False
        if opt_param is not None:
            upload = True
        return render_template('answer.html', name=u.name, images=questions, question=question, upload=upload, tested = u.tested)
