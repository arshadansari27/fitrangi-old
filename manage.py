import os, sys 

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask.ext.script import Manager, Server 
from app import app 

manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger = True, use_reloader = True, host = '0.0.0.0'))

@manager.command
def db_fixture():
    from app.fixture import db_fixture
    print "Run Database Fixtures\n", "*" * 80
    db_fixture()

if __name__ == '__main__':
    manager.run()
