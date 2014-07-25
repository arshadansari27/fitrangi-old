import simplejson as json
from app.models import *
from app import db
from BeautifulSoup import BeautifulSoup
import urllib2
import os, shutil, sys, hashlib
import StringIO, time
from PIL import Image as PILImage
from scripts.db_load import load_all
from mongoengine import Q
import mongoengine


def db_fixture(local):
    data = load_all(local)
    admin_type = UserType.objects(name__iexact="ADMIN").first()
    if not User.objects(email__iexact='arshadansari27@gmail.com').first():
        admin = User(name='Arshad Ansari', email='arshadansari27@gmail.com', password='testing', user_type=admin_type)
        admin_profile = Post(title='Arshad Ansari', content="", images=[], videos=[], tags=[], geo_location=None, post_type=PostType.objects(name__iexact='PROFILE').first()).save()
        admin.profile = admin_profile
        admin.save()


    admin = User.objects(user_type__iexact=admin_type).first()
    for d in data:
        title = d['title']
        __posttype = None
        if d['type'] in ['DEALER', 'ORGANISER']:
            user_type = UserType.objects(name__iexact=d['type']).first()
            user = User.objects(Q(name=d['title']) & Q(user_type=user_type)).first()
            if not user:
                user = User(name=d['title'], email='example@fitrangi.com', password='fitrangi@123', user_type=user_type)
                user.save()

            post_type = PostType.objects(name__iexact='PROFILE').first()
            __posttype = 'PROFILE'
        else:
            post_type = PostType.objects(name__iexact=d['type']).first()
            __posttype = d['type']
            user = None
        

        post = Post.objects(Q(title=d['title']) & Q(post_type=post_type)).first()

        if not post:
            post = Post(created_by=admin, title=title, post_type=post_type)
            if d.get('data', None) is not None:
                post.content=d['data']
        _tags = []
        if d.get('category', None) is not None:
            tag_1 = Tag.objects(name__iexact=d['category']).first()
            if tag_1 is not None:
                print tag_1.name
                _tags.append(tag_1)
            else:
                print 'No category', d['category']

        if d.get('activity', None) is not None:
            tag_2 = Tag.objects(name__iexact=d['activity']).first()
            if tag_2:
                print tag_2.name
                _tags.append(tag_2)
            else: 
                print "Not found", d['activity']
        post.tags = [_i for _i in _tags]
        images = []
        if d.get('image', None):
            image_path = d['image']
            print "I:", image_path
            name = unicode(str(image_path.split('/')[-1])).encode('utf-8')
            _name = hashlib.md5(name).hexdigest()
            new_name =  os.getcwd() + '/app/assets/files/media/images/%s' % _name
            images.append('/assets/files/media/images/%s' % _name)
            if not local or not os.path.exists(new_name):
                shutil.copy(image_path, new_name)

        post.images = [_j for _j in images]
        post.save()
        if __posttype == 'PROFILE' and user is not None:
            user.profile = post
            user.save()
