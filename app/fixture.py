import simplejson as json
from app.models import Node
from BeautifulSoup import BeautifulSoup
import urllib2
import os, shutil, sys, hashlib
import StringIO, time, datetime
from scripts.db_load import load_all
from app.models.page_types import generate_alias_wise_data, get_page_types


def db_fixture(local):
    _file = open('fixture.log', 'w')
    data = load_all(local)
    admins = Node.find({"type": "Admin"})
    created_nodes = 0
    if len(admins) is 0:
        print "not found' creating'"
        created_nodes += 1
        admin_data = {
            'name':'arshad', 'email': 'arshadansari27@gmail.com', 'phone': '2342342432423', 'address': '', 'website': '', 'facebook': '',
            'profile_image': None, 'linkedin': '', 'username': 'arshadansari27', 'password': 'testing', 'is_verified': True, 'type': 'Admin', 'created_on': datetime.datetime.now(),
            'followers': [], 'following': [], 
            'tags': ["enthusiast"]
        }
        admin = Node(admin_data)
        admin.save()
    else:
        admin = admins[0]
    print 'Admin ', admin.name
    
    aliases = generate_alias_wise_data()
    page_types = get_page_types()
    comparable_page_types = dict([(v.lower(), v) for v in page_types])
    for d in data:
        title = d['title']
        _type = aliases[d['type']]
        images = []
        if d.get('image', None):
            image_path = d['image']
            name = unicode(str(image_path.split('/')[-1])).encode('utf-8')
            _name = hashlib.md5(name).hexdigest()
            new_name =  os.getcwd() + '/app/assets/files/media/images/%s' % _name
            images.append('/assets/files/media/images/%s' % _name)
            if not local or not os.path.exists(new_name):
                shutil.copy(image_path, new_name)
            _file.write("%s\n%s\n%s\nBREAK\n" % (d['image'], _name, new_name))

        if _type in ['EventOrganiser', 'Enthusiast', 'Retailer']:

            node_data = {
                'name':title , 'email': '', 'phone': '', 'address': '', 'website': '', 'facebook': '', 'profile_image': images[0] if len(images) > 0 else None,
                'linkedin': '', 'username': title.lower().replace(' ', '-'), 'password': 'testing', 'is_verified': True, 
                'type': _type, 'created_on': datetime.datetime.now(), 'followers': [], 'following': [],  'tags': ["Enthusiast", _type]
            }
            query = {'name': title}
        else:
            tags = [_type]
            if d.get('category', None) is not None:
                category = d['category']
                if len(category) > 0 and comparable_page_types.has_key(category.lower()):
                    tags.append(comparable_page_types[category.lower()])

            if d.get('activity', None) is not None:
                activity = d['activity']
                if len(activity) > 0 and comparable_page_types.has_key(activity.lower()):
                    tags.append(comparable_page_types[activity.lower()])

           
            node_data = {
                'images': images, 'videos':[], 'created_by': admin,  
                'title': title, 'text': d['data'] if len(d.get('data', '')) > 0 else '', 'published_on': datetime.datetime.now(), 
                'is_published': True, 'type': _type, 'tags': tags, 'page_access': 'public',
                'related': []
            }
            query = {'title': title}
        
        if Node.find_count(query) > 0:
            node = Node.find(query)[0]
            node.update(node_data)     
        else:
            node = Node(node_data)
        node.save()
        created_nodes += 1

    print "Created Nodes: ", created_nodes
    _file.close()
