from flask import session
from types import Node; Node
from page_types import PAGE_TYPES
import hashlib, datetime
from flask import session, g

class User():
    def __init__(self, name, id, _type=None, anonymous=False):
        self.name = name
        self.id = str(id)
        self.type = _type
        self.is_anonymous = anonymous

    def __repr__(self):
        return "%s: %s [%s]" % (self.type, self.name, self.id)
 
    def is_admin(self):
        if self.type == 'Admin':
            return True
        return False

    @classmethod
    def get(cls, _id):
        if not _id:
            return None
        node = Node.get_by_id(_id)
        print "Got", node, '' if not node else node.type
        if node.type and PAGE_TYPES[node.type]['parent'] == 'Profile':
            return User(node.name, node._id, _type=node.type)
        else:
            _type = node.type
            while _type is not None and (PAGE_TYPES[_type]['parent'] != 'Profile' or PAGE_TYPES[_type]['parent'] is None):
                _type = PAGE_TYPES[_type]['parent']
                if PAGE_TYPES[_type] == 'Profile':
                    return User(node.name, node._id, _type=node.type)
        return None

    def logout_user(self):
        g.user = None
        if not session.has_key('login'):
            return True
        print "Removing", session.pop('login', None)
        return True

    @classmethod
    def authenticate(cls, email, password):
        password = hashlib.md5(password).hexdigest()
        nodes = Node.find({'email': email, 'password': password})
        print 'Authenticating', email, password, len(nodes)
        if not nodes or len(nodes) is 0:
            return None
        node = nodes[0]
        if node:
            user = User(node.name, node._id, node.type, False)
            session['login'] = {
                'id': str(node._id), 
                'timestamp': datetime.datetime.now(),
                'user_obj': user.__dict__
            }
            g.user = user
            print "***Authenticated", g.user
        else:
            g.user = None
        return g.user

    @classmethod
    def logged_in_user(cls):
        if not session.has_key('login'):
            return None
        session_info = session['login']
        user_dict = session_info['user_obj']
        if not user_dict:
            session.pop('login', None)
            return None
        g.user = User(user_dict['name'], user_dict['id'], user_dict['type'])
        print "INFO from session: ", g.user
        return g.user


class Service(object):

    @classmethod
    def get_default(cls, _type):
        if _type in ['Profile', 'Admin', 'EventOrganiser', 'Enthusiast', 'Retailer']:
            page_type = 'Profile'
        else:
            page_type = 'Post'
        if page_type == 'Post':
            return {
                'images': [], 'videos':[], 'created_by': None,  'created_on': datetime.datetime.now(),
                'title': None, 'text': '', 'published_on': None, 
                'is_published': False, 'type': _type, 'tags': list(set(['Enthusiast', _type])), 'page_access': 'public',
                'related': []
            }
        elif page_type == 'Profile':
            return {
                'name': None, 'email': None, 'phone': '', 
                'address': '', 'website': '', 
                'facebook': '', 'profile_image':  None,
                'linkedin': '', 'username': None, 'password': None, 'is_verified': False, 
                'type': page_type, 'created_on': datetime.datetime.now(), 'followers': [], 'following': [],  'tags': list(set(["Enthusiast", _type]))
            }
        else:
            raise Exception("Invalid Page Type")
       
    @classmethod
    def create_comment(cls, author_node, comment_text, post_node):
        comment_node = cls.get_default('Comment')
        comment_node['text'] = comment_text
        comment_node['created_by'] = str(author_node._id)
        comment_node['published_on'] = datetime.datetime.now()
        comment_node['is_published'] = True
        print "Adding comment for *********", post_node._id
        comment_node['belongs_to'] = str(post_node._id)
        node = Node(comment_node)
    
        node.save()
        print "Comment Created:", node._id
        return node

        

