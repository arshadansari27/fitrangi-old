import simplejson as json
import datetime
from flask import url_for
from app import db
from mongoengine import Q


class Node(db.Document):
    created_at  = db.DateTimeField(default=datetime.datetime.now, required=True)
    location    = db.StringField()

    def __unicode__(self):
        return self._id

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }

class Tag(Node):
    name        = db.StringField(required=True)
    category    = db.StringField(required=True)
    parent      = db.ReferenceField('Tag')

    def __unicode__(self):
        return "%s, %s" % (self.name, self.category)

    meta = {
        'allow_inheritance': True,
        'indexes': ['name']
    }

class ProductType(Node):
    name        = db.StringField(required=True)

    def __unicode__(self):
        return self.name

    meta = {
        'allow_inheritance': True,
        'indexes': ['name']
    }


class UserType(Node):
    name        = db.StringField(required=True)

    def __unicode__(self):
        return self.name

    meta = {
        'allow_inheritance': True,
        'indexes': ['name']
    }

    
class PostType(Node):
    name        = db.StringField(required=True)

    def __unicode__(self):
        return self.name

    meta = {
        'allow_inheritance': True,
        'indexes': ['name']
    }

class Post(Node):
    created_by      = db.ReferenceField('User')
    title           = db.StringField()
    content         = db.StringField()
    images          = db.ListField(db.StringField())
    videos          = db.ListField(db.StringField())
    tags            = db.ListField(db.ReferenceField(Tag))
    geo_location    = db.PointField()
    post_type       = db.ReferenceField(PostType)
    parent          = db.ReferenceField('Post')
    
    meta = {
        'allow_inheritance': True,
        'indexes': ['title']
    }
    
    def __unicode__(self):
        return self.title

class Product(Node):
    created_by      = db.ReferenceField('User')
    currency        = db.StringField()
    price           = db.FloatField()
    discountPrice   = db.FloatField()
    images          = db.ListField(db.ImageField())
    video           = db.FileField()
    title           = db.StringField()
    description     = db.StringField()
    options         = db.DictField()
    product_type    = db.ReferenceField(PostType)
    interested      = db.ListField(db.ReferenceField('User'))

    @property
    def percentageOff(self):
        return ((float(self.price) - float(self.discoutPrice)) / float(self.price)) * 100

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['title']
    }


class User(Node):
    name        = db.StringField(required=True)
    profile     = db.ReferenceField(Post)
    email       = db.EmailField(required=False)
    password    = db.StringField(required=False)
    phone       = db.StringField()
    addresss    = db.StringField()
    user_type   = db.ReferenceField('UserType')
    webite      = db.StringField()
    facebook    = db.StringField()
    verified    = db.BooleanField()
    tags        = db.ReferenceField(Tag)
    
    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email'],
        'ordering': ['-created_at']
    }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.name


USER_TYPE       = ['ADMIN',     'DEALER',   'ORGANISER',    'OUTDOOR PROFESSIONAL',     'ENTHUSIAST']
POST_TYPE       = ['PROFILE',   'BLOG',     'DESTINATION',  'ACTIVITY',                 "ARTICLE",      'COMMENT']
PRODUCT_TYPE    = ['EVENT',     'GEAR',     'OUTFITS']

for v in USER_TYPE:
    if UserType.objects(name__iexact=v):
        continue
    UserType(name=v).save()
    print UserType.objects(name__iexact=v).first()
print 'User Types', len(UserType.objects.all())

for v in POST_TYPE:
    if PostType.objects(name__iexact=v):
        continue
    PostType(name=v).save()
    print PostType.objects(name__iexact=v).first()
print 'Post Types', len(PostType.objects.all())

for v in PRODUCT_TYPE:
    if ProductType.objects(name__iexact=v):
        continue
    ProductType(name=v).save()
    print ProductType.objects(name__iexact=v).first()
print 'Product Types', len(ProductType.objects.all())


TAGS = [
        ("Rescuer",                        "SKILL",              None,),
        ("Trainer",                        "SKILL",              None,),
        ("LAND SPORTS",                    "ACTIVITY_TYPE",      None,),
        ("OTHER SPORTS",                   "ACTIVITY_TYPE",      None,),
        ("SKY - FLY",                      "ACTIVITY_TYPE",      None,),
        ("SNOW - FLOW",                    "ACTIVITY_TYPE",      None,),
        ("TRAVELLING & SIGHTSEEING",       "ACTIVITY_TYPE",      None,),
        ("WATER - WONDERS",                "ACTIVITY_TYPE",      None,),
        ("Export",                         "ARTICLE",            None,),
        ("Informative",                    "ARTICLE",            None,),
        ("Top 5 Series",                   "ARTICLE",           None,),
        ("Camping",                        "ACTIVITY",          "LAND SPORTS",),
        ("Cycling-Biking",                 "ACTIVITY",          "LAND SPORTS",),
        ("Marathons",                      "ACTIVITY",          "LAND SPORTS",),
        ("Mountaineering",                 "ACTIVITY",          "LAND SPORTS",),
        ("Off-beat Activities",            "ACTIVITY",          "LAND SPORTS",),
        ("Rappelling & Valley Crossing",   "ACTIVITY",          "LAND SPORTS",),
        ("Rock Climbing",                  "ACTIVITY",          "LAND SPORTS",),
        ("Trekking & Hiking",              "ACTIVITY",          "LAND SPORTS",),
        ("Horse Riding",                   "ACTIVITY",          "OTHER SPORTS",),
        ("Stargazing",                     "ACTIVITY",          "OTHER SPORTS",),
        ("Zorbing",                        "ACTIVITY",          "OTHER SPORTS",),
        ("Bungee jumping",                 "ACTIVITY",          "SKY - FLY",),
        ("Hang Gliding",                   "ACTIVITY",          "SKY - FLY",),
        ("Hot Air Ballooning",             "ACTIVITY",          "SKY - FLY",),
        ("Para Motoring",                  "ACTIVITY",          "SKY - FLY",),
        ("Paragliding",                    "ACTIVITY",          "SKY - FLY",),
        ("Parasailing",                    "ACTIVITY",          "SKY - FLY",),
        ("Sky Diving",                     "ACTIVITY",          "SKY - FLY",),
        ("Zip Line",                       "ACTIVITY",          "SKY - FLY",),
        ("Architecture Monuments",         "ACTIVITY",          "TRAVELLING & SIGHTSEEING",),
        ("Beaches",                        "ACTIVITY",          "TRAVELLING & SIGHTSEEING",),
        ("Forts & Caves",                  "ACTIVITY",          "TRAVELLING & SIGHTSEEING",),
        ("Hill stations",                  "ACTIVITY",          "TRAVELLING & SIGHTSEEING",),
        ("Places to Visit",                "ACTIVITY",          "TRAVELLING & SIGHTSEEING",),
        ("Theme Parks",                    "ACTIVITY",          "TRAVELLING & SIGHTSEEING",),
        ("Wildlife Sanctuaries & Safaris", "ACTIVITY",          "TRAVELLING & SIGHTSEEING",),
        ("Canyoning",                      "ACTIVITY",          "WATER - WONDERS",),
        ("Kayaking",                       "ACTIVITY",          "WATER - WONDERS",),
        ("Kite Surfing",                   "ACTIVITY",          "WATER - WONDERS",),
        ("Scuba Diving",                   "ACTIVITY",          "WATER - WONDERS",),
        ("Snorkelling",                    "ACTIVITY",          "WATER - WONDERS",),
        ("Surfing",                        "ACTIVITY",          "WATER - WONDERS",),
        ("Water Rafting",                  "ACTIVITY",          "WATER - WONDERS",),
]


for (i, j, k,) in TAGS:
    tag = Tag.objects(Q(name=i) & Q(category=j)).first()
    if tag is not None:
        if k:
            if tag.parent.name == k:
                continue
            else:
                tag.parent = Tag.object(name__iexact=k).first()
        else:
            continue
    else:
        tag = Tag(name=i, category=j)
        if k:
            parent = Tag.objects(name__iexact=k).first()
            if not parent:
                raise Exception("Parent must be created first")
        else:
            parent = None
        if k and parent:
            tag.parent = parent
    print tag
    tag.save()

print "Tags: ", len(Tag.objects.all())

