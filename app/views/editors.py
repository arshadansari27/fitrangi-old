from flask import Blueprint, request, redirect, render_template, url_for, abort, flash, g
from flask.views import MethodView
#from app.models import Node
from config import configuration
from utils import json_converter, login_required, admin_required, PublicEditView, PrivateEditView, AdminEditView

from app.models import Node, User

url_prefixes = {}
for k, v in configuration['editors'].iteritems():
    url_prefix = v['url-prefix']
    url_prefixes[url_prefix] = {'name': k, 'page-type': v['page-type'], 'fields': v['fields']}

class LoginView(PublicEditView):

    def post(self):
        payload = request.json or {}
        print '*' * 100
        print "JSON", request.json
        print payload
        print '*' * 100
        email, password = payload.get('email'), payload.get('password')
        user = User.authenticate(email, password)
        if user:
            #flash('Successfully logged in', category='success')
            return {'status': 'success', 'node': user.__dict__, "message": "Successfully logged in"}
        else:
            #flash('Unable to log you in', category='error')
            return {'status': 'error', 'node': None, 'message': 'Unable to log you in'}

class LogoutView(PrivateEditView):
    def post(self):
        print '*****', g.user, g.user.id
        user = User.logged_in_user() 
        if user:
            print "Logging out", user.id
            if user.logout_user():
                return {'status': 'success', 'message': 'Logout successfull'}

        return {'status': 'error', 'message': 'Something went bad'}

"""
class Bananas(EditView):
 
    def post(self, url_prefix, key=None):
        '''Create new banana.'''
        payload = request.json or {}
        banana_type, name = payload.get('type'), payload.get('name')
        farm_id = payload.get('farm') or farm_id
        if not banana_type or not name or not farm_id:
            raise BadRequest('"type", "farm" and "name" are required.')
 
        return bananas.new(banana_type=banana_type, name=name, farm_id=farm_id)

the_api = Blueprint('the_api', __name__)
the_api.add_url_rule('/bananas', view_func=Bananas.as_view('bananas'))
the_api.add_url_rule('/farm/<farm_id>/bananas', view_func=Bananas.as_view('bananas_from_a_farm'))
"""
the_api = Blueprint('the_api', __name__, template_folder='templates')
the_api.add_url_rule('/login', view_func=LoginView.as_view('login'))
the_api.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
