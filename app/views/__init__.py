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

from app.views.pages import activities, destinations, events, organisers, dealers, blogs

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
    if Activity.objects.count() >= 6:
        activities = Activity.objects.all()[0:6]
    else:
        activities = Activity.objects.all()
    if Destination.objects.count() >= 6:
        destinations = Destination.objects.all()[0:6]
    else:
        destination = Destination.objects.all()
    if TripOrganiser.objects.count() >= 6:
        organisers = TripOrganiser.objects.all()[0:6]
    else:
        organisers = TripOrganiser.objects.all()
    if GearDealer.objects.count() >= 6:
        dealers = GearDealer.objects.all()[0:6]
    else:
        dealers = GearDealer.objects.all()
    if Blog.objects.count() >= 6:
        blogs = Blog.objects.all()[0:6]
    else:
        blogs = Blog.objects.all()

    return render_template('index.html', activities=activities, destinations=destinations, dealers=dealers, blogs=blogs, organisers=organisers)

@app.route('/files/img/<id>')
def serve_gridfs_file(id):
    try:
        db = get_db()	
        gfs = GridFS(db, collection='images')
        fl = gfs.get(ObjectId(id))
        print fl
        response = make_response(fl.read())
        response.mimetype = fl.content_type
        return response
    except NoFile:
        print 'Error occured'
        abort(404)



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



