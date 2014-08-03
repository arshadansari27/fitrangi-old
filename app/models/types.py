import datetime, pymongo
from bson.objectid import ObjectId
from app.settings import HOST, PORT, DB


client = pymongo.MongoClient(HOST, PORT)
db = client[DB]


class Node(object): 

    collection = 'NODE'

    def __init__(self, kwargs={}):
        if len(kwargs) == 0:
            return 
        if not kwargs.has_key('created_on'):
            kwargs['created_on'] = datetime.datetime.now()

        if kwargs.has_key('_id'):
            self.__dict__['_id'] = kwargs['_id']
        page_type = kwargs['type']
        from page_types import get_attributes_for
        attributes = get_attributes_for(page_type)
        for attribute in attributes:
            _name = attribute[0]
            self.__dict__.setdefault(_name, None)
            if kwargs.get(_name, None):
                self.__dict__[_name] = kwargs[_name]

    def __getattr__(self, attr):
        value = None
        if self.__dict__.has_key(attr):
            value = self.__dict__[attr]
        if value:
            if type(value) == ObjectId:
                value = Node.get_by_id(value)
        return value

    @classmethod
    def __node_from_doc(cls, doc):
        return Node(doc)

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
    def find(cls, query, limit=None):
        if limit:
            return [Node.__node_from_doc(v) for v in db[Node.collection].find(query).limit(limit)]
        else:
            return [Node.__node_from_doc(v) for v in db[Node.collection].find(query)]

    @classmethod
    def find_count(cls, query):
        return db[Node.collection].find(query).count()

    def update(self, kwargs):
        for k, v in kwargs.iteritems():
            self.__dict__[k] = v

    def save(self):
        for key, value in self.__dict__.iteritems():
            if type(value) == Node:
                if value.__dict__.has_key('_id') and value.__dict__['_id'] is None:
                    del value.__dict__['_id']
                    value_id = value.save()
                    self.__dict__[key] = value_id
                else:
                    self.__dict__[key] = value._id
        if not self.__dict__.has_key('_id'):
            _id = db[Node.collection].insert(self.__dict__)
            self = db[Node.collection].find_one({'_id': _id})
        elif self.__dict__.has_key('_id') and self.__dict__['_id'] is None:
            del self.__dict__['_id']
            _id = db[Node.collection].insert(self.__dict__)
            self = db[Node.collection].find_one({'_id': _id})
        else:
            db[Node.collection].update({'_id': self._id}, self.__dict__, upsert=True)
                    



def print_post_details(node):
    print '*' * 100
    print node._id, node.title, node.images, node.created_by, node.text

def print_profile_details(node):
    print '*' * 100
    print node._id,
    print node.name,node.email, node.phone,node.address, node.website, node.facebook, node.linkedin, 
    print node.username, node.password, node.is_verified, node.type, node.created_on, 
    print node.followers, node.following, node.tags, 


if __name__ == '__main__':
    #admin = 53dcecdadc7006655b945573
    """
    print_post_details(node)
    author = node.created_by
    print author, type(author), node.__types__['_created_by']
    print_profile_details(author)

    """
    admin = {
            'name':'Arshad', 'email': 'arshadansari27@gmail.com', 'phone': '2342342432423', 'address': '', 'website': '', 'facebook': '',
            'linkedin': '', 'username': 'arshadansari27', 'password': 'testing', 'is_verified': True, 'type': 'Admin', 'created_on': datetime.datetime.now(),
            'followers': [], 'following': [], 
            'tags': ["Enthusiast"]
    }

    #node = Node(admin)
    """
    node = Node.get_by_id('53dd0fd3dc7006692158d591')
    print_profile_details(node)
    node.name = 'Mohammed Arshad Ansari'
    node.save()
    print '**', node._id, node.id, node.name
    """
    node = Node.find({'name': {'$regex':'Arshad'}})[0]
    print_profile_details(node) 
    post = {
        'images': [], 'videos':[], 'created_by': node, 
        'title': 'Test Blog', 'text': 'This is a test post', 'published_on': datetime.datetime.now(), 
        'is_published': True, 'type': 'Blog', 'tags': [], 'page_access': 'public',
        'related': []
    }

    np = Node(post)
    np.save()
    print_post_details(np)
    node = np.created_by
    if node:
        print_profile_details(node)
