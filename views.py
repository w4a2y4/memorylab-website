from flask import render_template
from main import app
from models import db, User, Link, Question, Team, TestUser, Settings
import urllib.request
import json

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


@app.route('/chatbot', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "I'm chatbot. owo)/", 200


@app.route('/chatbot', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    # log(data)
    for entry in data["entry"]:
        for messaging_event in entry["messaging"]:
            if messaging_event.get("message"):
                message = messaging_event["message"]
                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]
                u = TestUser.query.filter_by(fb_id=sender_id).first()
                if message.get('attachments'):
                    if u.tested == False:  # haven't answer
                        send_message(sender_id, "收到你的答案了～")
                        u.tested = True
                        for attachments in message['attachments']:
                            url = attachments['payload']['url']
                            urllib.request.urlretrieve(
                                url, "static/questions/")
                            sequence = json.loads(u.sequence)
                            q = Question.query.filter_by(
                                id=u.answering).first()
                            q.path = url[url.rfind("/")+1:url.find("?")]
                    else:
                        send_message(sender_id, "欸欸，你已經回答過囉")
                    db.session.commit()
                else:
                    message_text = message["text"]
                    send_message(sender_id, "嗨！這裡是記憶實驗所")
                    # send_message(sender_id, "喵。")
    return "ok", 200
