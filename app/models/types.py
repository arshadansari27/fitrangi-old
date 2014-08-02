import datetime, pymongo
from bson.objectid import ObjectId


client = pymongo.MongoClient('localhost', 27017)
db = client.new_fitrangi


class Node(object): 

    collection = 'NODE'

    def __init__(self, kwargs={}):
        if len(kwargs) == 0:
            return 
        page_type = kwargs['type']
        if not kwargs.has_key('created_on'):
            kwargs['created_on'] = datetime.datetime.now()

        self._my_types__ = {}
        self.id = None
        from page_types import get_attributes_for
        attributes = get_attributes_for(page_type)
        for attribute in attributes:
            _name, _type, _our_type, _collection = attribute
            try:
                assert kwargs.has_key(_name)
                assert type(kwargs[_name]) in [_type, _collection, Node]
            except Exception, e:
                print e, _name, _type, _collection
                raise e
            value = kwargs[_name]
            if type(value) == Node:
                if value.id is not None:
                    self.__dict__['_%s' % _name] = value.id
                else:
                    self.__dict__['_%s_obj' % _name] = value
            else:
                self.__dict__['_%s' % _name] = value
            converted = str(_type)
            s_i = converted.find("'")
            e_i = converted.find("'", s_i + 1)
            _type = converted[s_i + 1: e_i]
            
            self.__my_types__['_%s' % _name] = _type.replace('__main__.', '')

    def getType(self, attr):
        _actual_attr = '_%s' % attr
        if self.__my_types__.get(_actual_attr, None):
            return eval(self.__my_types__[_actual_attr])
        return None

    @classmethod
    def __node_from_doc(cls, doc):
        n = Node()
        for k, v in doc.iteritems():
            n.__dict__[k] = v
        return n

    @classmethod
    def get_by_id(cls, id):
        doc = db[Node.collection].find_one({'_id': ObjectId(id)})
        return Node.__node_from_doc(doc)

    @classmethod
    def get_all(cls):
        return [Node.__node_from_doc(v) for v in db[Node.collection].find()]

    @classmethod
    def get_all_count(cls):
        return db[Node.collection].count()

    @classmethod
    def find(cls, query):
        return [Node.__node_from_doc(v) for v in db[Node.collection].find(query)]

    @classmethod
    def find_count(cls, query):
        return db[Node.collection].find(query).count()

    def __getattr__(self, attr):
        _actual_attr = '_%s' % attr
        if _actual_attr not in self.__dict__:
            raise AttributeError(attr)
        if not (attr == 'id' or attr=='_id'):
            _type = self.__my_types__[_actual_attr]
            if _type == Node:
                value = self.__dict__[_actual_attr]
                if (type(value) == list):
                    return [Node.get_by_id(v) for v in value]
                return Node.get_by_id(value)
        value = self.__dict__[_actual_attr]
        if type(value) == ObjectId:
            return Node.get_by_id(str(value))      
        return value

    def __setattr__(self, attr, value):
        if type(value) == Node :
            if hasattr(value, '_id'):
                self.__dict__['_%s' % attr] = value._id
            else:
                self.__dict__['_%s_obj' % attr] = value
        elif type(value) == list and len(value) > 0 and type(value[0]) == Node:
            for v in value:
                if hasattr(v, '_id'):
                    self.__dict__['_%s' % attr] = v._id
                else:
                    self.__dict__['_%s_obj' % attr] = v
        else:
            self.__dict__['_%s' % attr] = value

    def save(self):
        to_remove_obj = []
        for key in self.__dict__.keys():
            print 'Saving others inside', key, self.__dict__[key]
            if key.find('_obj') > -1:
                to_save_obj = self.__dict__[key]
                obj_id = to_save.save()
                self.__dict__[key[:key.find('_obj')]] = obj_id
                to_remove_obj(key)
        for key in to_remove_obj:
            del self.__dict__[key]
        if self._id is None:
            del self._id
            self._id = str(db[Node.collection].insert(self.__dict__))
        else:
            print 'updating this object'
            db[Node.collection].update({'_id': self._id}, self, upsert=True)
                    



def print_post_details(node):
    print '*' * 100
    print node.id, node.getType('id')
    print node.title, node.getType('title')
    print node.images, node.getType('images')
    print node.created_by, node.getType('created_by')
    print node.text, node.getType('text')

def print_profile_details(node):
    print '*' * 100
    print node.id, node.getType('id')
    print node.name, node.getType('name')
    print node.email, node.getType('email')
    print node.phone, node.getType('phone')
    print node.address, node.getType('address')
    print node.website, node.getType('website')
    print node.facebook, node.getType('facebook')
    print node.linkedin, node.getType('linkedin')
    print node.username, node.getType('username')
    print node.password, node.getType('password')
    print node.is_verified, node.getType('is_verified')
    print node.type, node.getType('type')
    print node.created_on, node.getType('created_on')
    print node.followers, node.getType('followers')
    print node.following, node.getType('following')
    print node.tags, node.getType('tags')
    print '*' * 100


if __name__ == '__main__':
    #admin = 53dcecdadc7006655b945573
    node = Node.get_by_id('53dcfe2fdc70066694a9e8d2')
    print_post_details(node)
    author = node.created_by
    print author, type(author), node.__my_types__['_created_by']
    print_profile_details(author)

    """
    post = {
        'images': [], 'videos':[], 'created_by': node, 
        'title': 'Test Blog', 'text': 'This is a test post', 'published_on': datetime.datetime.now(), 
        'is_published': True, 'type': 'Blog', 'tags': [], 'page_access': 'public',
        'related': []
    }
    print_profile_details(node)

    np = Node(post)
    np.save()
    print_post_details(np)

    nodes = Node.find({'_name': 'Arshad'})
    admin = {
            'name':'Arshad', 'email': 'arshadansari27@gmail.com', 'phone': '2342342432423', 'address': '', 'website': '', 'facebook': '',
            'linkedin': '', 'username': 'arshadansari27', 'password': 'testing', 'is_verified': True, 'type': 'Admin', 'created_on': datetime.datetime.now(),
            'followers': [], 'following': [], 
            'tags': ["Enthusiast"]
    }

    node = Node(admin)
    node.save()
    print node._id
    for node in nodes:
        print_profile_details(node) 
    test = ['Surfing', 'Product', 'Event', 'Professional', 'Enthusiast', 'Retailer']
    print '*' * 100
    for t in test:
        attributes = get_attributes_for(t)
        print '\n'.join([str(v) for v in attributes])
        print '*' * 100
    """
