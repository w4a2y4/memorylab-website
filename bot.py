# coding=UTF-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Question, Team, Evolution, TestUser, TestAnswer
from messenger_bot import send_message
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

sched = BlockingScheduler()

# Start at 12:30 
# @sched.scheduled_job('cron', hour='12', minute='30')
@sched.scheduled_job('cron', day_of_week='mon-sun', hour='0-23', minute='00-59', second='*/3')  
def send_all_task():
    # log("====send all====")
    users = User.query.all()
    testUsers = TestUser.query.all()
    for u in testUsers:
        send_message(u.fb_id, "Hey")

# Notice at 19:30 
@sched.scheduled_job('cron', hour='19', minute='30')
def notice_for_tester():
    # log("====notice====")
    testUser = TestUser.query.all()
    for u in testUser:
        send_message(u.fb_id, "快來回答吧。")

# End at 24:30 (00:30)
@sched.scheduled_job('cron', hour='00', minute='30')
def end_for_test():
    # log("====notice====")
    testUser = TestUser.query.all()
    for u in testUser:
        u.tested = False
        db.session.commit()

print("===========START===========")
sched.start()


# users = User.query.all()
# testUsers = TestUser.query.all()
# for u in testUsers:
#     send_message(u.fb_id, "Hey")