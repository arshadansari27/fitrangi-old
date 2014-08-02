from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext import admin
from flask.ext.admin.form import rules
from flask.ext.admin.contrib.mongoengine import ModelView
import os

#files_path = os.path.join(os.path.dirname(__file__), 'files')
app = Flask(__name__, template_folder='templates', static_folder='assets')
app.config['SECRET_KEY'] = '123456790'
#app.config['MONGODB_SETTINGS'] = {'DB': 'fitrangi-db'}
#db = MongoEngine(app)
#admin = admin.Admin(app, 'Fitrangi Data')

"""
from flask.ext import login
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
def init_login():
    from app.models import User
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(pk=user_id).first()
"""
def register_blueprints(app):
    # Prevents circular imports
    from app.views import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

"""
def start_app():
    import logging 
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    from app.models import *
    admin.add_view(ModelView(UserType))
    admin.add_view(ModelView(PostType))
    admin.add_view(ModelView(ProductType))
    admin.add_view(ModelView(User))
    admin.add_view(ModelView(Post))
    admin.add_view(ModelView(Product))
    admin.add_view(ModelView(Tag))

init_login()
start_app()
"""
register_blueprints(app)
