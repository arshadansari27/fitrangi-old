from flask import render_template, make_response, abort, request, g, flash, redirect, url_for
from app import app
from mongoengine.fields import get_db
from bson import ObjectId
from gridfs import GridFS
from gridfs.errors import NoFile
from wtforms import form, fields, validators
from flask.ext import login
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.admin import helpers, expose
from app.models import *

from app.views.pages import activities, destinations, events, organisers, dealers, articles

@app.context_processor
def inject_user():
    return dict(user=g.user if hasattr(g, 'user') else None)

@app.before_request
def before_request():
    if current_user and current_user.is_authenticated():
        g.user = current_user 
    else:
        g.user = None

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout_view():
    logout_user()
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
    activity = PostType.objects(name__iexact='ACTIVITY').first()
    if Post.objects(post_type=activity).count() >= 6:
        activities = Post.objects(post_type=activity).all()[0:6]
    else:
        activities = Post.objects(post_type=activity).all()
    destination = PostType.objects(name__iexact='DESTINATION').first()
    if Post.objects(post_type=destination).count() >= 6:
        destinations = Post.objects(post_type=destination).all()[0:6]
    else:
        destination = Post.objects(post_type=destination).all()
    organiser = PostType.objects(name__iexact='ORGANISER').first()
    if Post.objects(post_type=organiser).count() >= 6:
        organisers = Post.objects(post_type=organiser).all()[0:6]
    else:
        organisers = Post.objects(post_type=organiser).all()
    dealer = PostType.objects(name__iexact='DEALER').first()
    if Post.objects(post_type=dealer).count() >= 6:
        dealers = Post.objects(post_type=dealer).all()[0:6]
    else:
        dealers = Post.objects(post_type=dealer).all()
    article = PostType.objects(name__iexact='ARTICLE').first()
    if Post.objects(post_type=article).count() >= 6:
        articles = Post.objects(post_type=article).all()[0:6]
    else:
        articles = Post.objects(post_type=article).all()
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



