from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext import admin
#from flask.ext.admin.form import rules
import os

app = Flask(__name__, template_folder='templates', static_folder='assets')
app.config['SECRET_KEY'] = os.urandom(24)
app.debug = True

from flask.ext import login

def register_blueprints(app):
    from app.views import blueprints
    from app.views import the_api
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    app.register_blueprint(the_api)

def start_app():
    from app.views.sessions import MongoSessionInterface
    from app.models import *
    import logging 
    app.session_interface = MongoSessionInterface()
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

start_app()
register_blueprints(app)
