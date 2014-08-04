from flask import render_template, make_response, abort, request, g, flash, redirect, url_for
from app import app
from app.models import Node
from bson import ObjectId
from wtforms import form, fields, validators
from app.models import *

from app.views.pages import blueprints
from app.views.editors import the_api
from app.views.utils import login_required

@app.before_request
def before_request():
    if not hasattr(g, 'user') or g.user is None:
        g.user = User.logged_in_user()
        if not g.user:
            return

@app.route('/slider_test', methods=['GET'])
def slider():
    return render_template('slider.html')

@app.route('/post_editor/<key>', methods=['GET'])
def edit_post(key):
    if not hasattr(g, 'user') or g.user is None:
        return redirect(url_for('index'))
    node = Node.get_by_id(key)
    back = request.referrer
    return render_template('post/editor.html', post=node, back=back)

@app.route('/profile_editor/<key>', methods=['GET'])
def edit_profile(key):
    if not hasattr(g, 'user') or g.user is None:
        return redirect(url_for('index'))
    node = Node.get_by_id(key)
    back = request.referrer
    return render_template('user/editor.html', profile=node, back=back)


@app.route('/', methods=['GET', 'POST'])
def index():
    activities = Node.find({'type':'Activity'}, limit=6)
    destinations = Node.find({'type': "Destination"}, limit=6)
    organisers = Node.find({"type": "EventOrganiser"}, limit=6)
    dealers = Node.find({"type": "Retailer"}, limit=6)
    articles = Node.find({"type": {"$in": ["Blog", "FitrangiSpecial"]}}, limit=6)
    return render_template('index.html', activities=activities, destinations=destinations, dealers=dealers, articles=articles, organisers=organisers)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')
