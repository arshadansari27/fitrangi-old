from flask import Blueprint, request, redirect, render_template, url_for, abort, flash, g
from flask.views import MethodView
from app.models import Node, Service
from config import configuration
from utils import json_converter, login_required, admin_required, PublicEditView, PrivateEditView, AdminEditView
from base64 import decodestring, b64decode
import os, urllib, binascii

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
        user = User.logged_in_user() 
        if user:
            print "Logging out", user.id
            if user.logout_user():
                return {'status': 'success', 'message': 'Logout successfull'}

        return {'status': 'error', 'message': 'Something went bad'}

class CommentEditor(PrivateEditView):

    def post(self):
        user = User.logged_in_user() 
        if user:
            payload = request.json or {}
            comment = payload.get('comment')
            post_key    = payload.get('key')
            author = Node.get_by_id(user.id)
            post = Node.get_by_id(post_key)
            comment_node = Service.create_comment(author, comment, post)
            return {'status': 'success', 'node': comment_node, 'message': 'Successfully posted the comment'}
        else:
            return {'status': 'error', 'message': 'Please login first.'}

class CommentEditor(PrivateEditView):

    def post(self):
        user = User.logged_in_user() 
        try:
            if user:
                payload = request.json or {}
                post_key    = payload.get('key')
                title = payload.get('title')
                text = payload.get('text')
                published = payload.get('published')
                image = payload.get('image')
                post = Node.get_by_id(post_key)
                post.title = title
                post.text = text 
                post.published = published
                post.save()
                if image:
                    try:
                        if image:
                            image = image[image.index(',') + 1:]
                            with open(os.getcwd() + '/app' + post.images[0],"wb") as f:
                                f.write(image.decode('base64'))
                    except Exception, e:
                        print str(e)
                        return {'status': 'error', 'message': 'Update the data but image could not be saved'}
                return {'status': 'success', 'node': post, 'message': 'Successfully updated the post'}
            else:
                return {'status': 'error', 'message': 'Please login first.'}
        except:
            return {'status': 'error', 'message': 'Something went wrong.'}



the_api = Blueprint('the_api', __name__, template_folder='templates')
the_api.add_url_rule('/login', view_func=LoginView.as_view('login'))
the_api.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
the_api.add_url_rule('/comment', view_func=CommentEditor.as_view('comment'))
the_api.add_url_rule('/post_edit', view_func=CommentEditor.as_view('post_edit'))
