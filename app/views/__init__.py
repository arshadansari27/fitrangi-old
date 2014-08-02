from flask import render_template, make_response, abort, request, g, flash, redirect, url_for
from app import app
from app.models import Node
from mongoengine.fields import get_db
from bson import ObjectId
from gridfs import GridFS
from gridfs.errors import NoFile
from wtforms import form, fields, validators
from flask.ext import login
#from flask.ext.login import login_required, login_user, logout_user, current_user
#from flask.ext.admin import helpers, expose
from app.models import *

from app.views.pages import blueprints

@app.context_processor
def inject_user():
    return dict(user=g.user if hasattr(g, 'user') else None)

@app.before_request
def before_request():
    """
    if current_user and current_user.is_authenticated():
        g.user = current_user 
    else:
    """
    g.user = None

@app.route('/logout', methods=['GET', 'POST'])
#@login_required
def logout_view():
    #logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not helpers.validate_form_on_submit(form):
            flash('Invalid form data', category='danger')
            return redirect(url_for('login'))
        user = form.get_user()
        if not user:
            flash('Invalid credentials, user not found', category='danger')
            return redirect(url_for('login'))
        login_user(user)
        if not current_user.is_authenticated():
            flash('Invalid credentials, user not authenticated', category='danger')
            return redirect(url_for('login'))
        flash('Welcome, %s' % current_user.name, category='success')
        g.user = current_user
        return redirect(url_for('index'))
    return render_template('login.html', login_form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    activities = Node.find({'type':'Activity'}, limit=6)
    destinations = Node.find({'type': "Destination"}, limit=6)
    organisers = Node.find({"type": "EventOrganiser"}, limit=6)
    dealers = Node.find({"type": "Retailer"}, limit=6)
    articles = Node.find({"type": {"$in": ["Blog", "FitrangiSpecial"]}}, limit=6)
    return render_template('index.html', activities=activities, destinations=destinations, dealers=dealers, articles=articles, organisers=organisers)

class LoginForm(form.Form):
    username = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        urs = User.objects(email__iexact=self.username.data.strip()).first()
        print 'Found user', urs
        if urs and urs.password == self.password.data.strip():
            print 'Password matched'
            return urs
        return None

class RegistrationForm(form.Form):
    name = fields.TextField(validators=[validators.required()])
    email = fields.TextField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if User.objects(email__iexact=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')



