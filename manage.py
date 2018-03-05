from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from main import app, db
from models import User, Question

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Question=Question, Team=Team)

if __name__ == '__main__':
    manager.run()
