from flask import Blueprint, make_response, json, g, request
from bson import ObjectId
from flask.views import MethodView
from pymongo.errors import DuplicateKeyError
from werkzeug import exceptions
from app.models import User, Node

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, Node):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

def handle_exception(e):
    # handle common exceptions
    if isinstance(e, DuplicateKeyError):
        raise BadRequest(str(e))
 
 
def json_converter(f):
    '''Converts `dict`, list or mongo cursor to JSON.
    Creates `~flask.Response` object and sets headers.
    '''
    def decorator(*args, **kwargs):
        try:
            print 'JSON CONVERSION DECORATION'
            result = f(*args, **kwargs)
        except Exception as e:
            handle_exception(e)
            raise
 
        if isinstance(result, dict):
            print '**** dumping', result
            result = json.dumps(result, cls=JsonEncoder)
        else:
            # unwind cursor
            print '**** manipulting first', result
            result = json.dumps(list(result), cls=JsonEncoder)
        response = make_response(result)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    return decorator
 
 
def login_required(f):
    def decorator(*args, **kwargs):
        print 'lOGIN REQUIRED DECORATION'
        user = User.logged_in_user()
        if not user:
            return {'status': 'error', 'status_code': 401, 'message':'You must log in to access this URL.'}
        return f(*args, **kwargs)
    return decorator
 
 
def admin_required(f):
    def decorator(*args, **kwargs):
        user = g.user
        if not user or not user.is_admin():
            print 'Returning Dict Response from admin required check'
            return {'status': 'error', 'status_code':403, 'message':'You must log in as admin to access this URL.'}
        return f(*args, **kwargs)
    return decorator
 
class PublicEditView(MethodView):
    decorators = [json_converter]

class PrivateEditView(MethodView):
    decorators = [login_required, json_converter]

class AdminEditView(MethodView):
    decorators = [admin_required, login_required, json_converter]
