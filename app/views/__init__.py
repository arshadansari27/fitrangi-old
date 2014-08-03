from flask import render_template, make_response, abort, request, g, flash, redirect, url_for
from app import app
from app.models import Node
from bson import ObjectId
from wtforms import form, fields, validators
from app.models import *

from app.views.pages import blueprints
from app.views.editors import the_api
from app.views.utils import login_required

@app.context_processor
def inject_user():
    return dict(user=g.user if hasattr(g, 'user') else None)

@app.before_request
def before_request():
        g.user = User.logged_in_user()

@app.route('/slider_test', methods=['GET'])
def slider():
    return render_template('slider.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    activities = Node.find({'type':'Activity'}, limit=6)
    destinations = Node.find({'type': "Destination"}, limit=6)
    organisers = Node.find({"type": "EventOrganiser"}, limit=6)
    dealers = Node.find({"type": "Retailer"}, limit=6)
    articles = Node.find({"type": {"$in": ["Blog", "FitrangiSpecial"]}}, limit=6)
    return render_template('index.html', activities=activities, destinations=destinations, dealers=dealers, articles=articles, organisers=organisers)
