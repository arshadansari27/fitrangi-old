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
    print UserType.objects(name__iexact=v)
print 'User Types', len(UserType.objects.all())

for v in POST_TYPE:
    if PostType.objects(name__iexact=v):
        continue
    PostType(name=v).save()
    print PostType.objects(name__iexact=v)
print 'Post Types', len(PostType.objects.all())

for v in PRODUCT_TYPE:
    if ProductType.objects(name__iexact=v):
        continue
    ProductType(name=v).save()
    print ProductType.objects(name__iexact=v)
print 'Product Types', len(ProductType.objects.all())


TAGS = {
        "Rescuer"                       : "SKILLS",
        "Trainer"                       : "SKILLS",
        "LAND SPORTS"                   : "ACTIVITY",
        "OTHER SPORTS"                  : "ACTIVITY",
        "SKY - FLY"                     : "ACTIVITY",
        "SNOW - FLOW"                   : "ACTIVITY",
        "TRAVELLING & SIGHTSEEING"      : "ACTIVITY",
        "WATER - WONDERS"               : "ACTIVITY",
        "Export"                        : "ARTICLES",
        "Informative"                   : "ARTICLES",
        "Top 5 Series"                  : "ARTICLES",
        "Camping"                       : "LAND SPORTS",
        "Cycling-Biking"                : "LAND SPORTS",
        "Marathons"                     : "LAND SPORTS",
        "Mountaineering"                : "LAND SPORTS",
        "Off-beat Activities"           : "LAND SPORTS",
        "Rappelling & Valley Crossing"  : "LAND SPORTS",
        "Rock Climbing"                 : "LAND SPORTS",
        "Trekking & Hiking"             : "LAND SPORTS",
        "Horse Riding"                  : "OTHER SPORTS",
        "Stargazing"                    : "OTHER SPORTS",
        "Zorbing"                       : "OTHER SPORTS",
        "Bungee jumping"                : "SKY - FLY",
        "Hang Gliding"                  : "SKY - FLY",
        "Hot Air Ballooning"            : "SKY - FLY",
        "Para Motoring"                 : "SKY - FLY",
        "Paragliding"                   : "SKY - FLY",
        "Parasailing"                   : "SKY - FLY",
        "Sky Diving"                    : "SKY - FLY",
        "Zip Line"                      : "SKY - FLY",
        "Skiing & Snowboarding"         : "SNOW - FLOW",
        "Architecture Monuments"        : "TRAVELLING & SIGHTSEEING",
        "Beaches"                       : "TRAVELLING & SIGHTSEEING",
        "Forts & Caves"                 : "TRAVELLING & SIGHTSEEING",
        "Hill stations"                 : "TRAVELLING & SIGHTSEEING",
        "Places to Visit"               : "TRAVELLING & SIGHTSEEING",
        "Theme Parks"                   : "TRAVELLING & SIGHTSEEING",
        "Wildlife Sanctuaries & Safaris": "TRAVELLING & SIGHTSEEING",
        "Canyoning"                     : "WATER - WONDERS",
        "Kayaking"                      : "WATER - WONDERS",
        "Kite Surfing"                  : "WATER - WONDERS",
        "Scuba Diving"                  : "WATER - WONDERS",
        "Snorkelling"                   : "WATER - WONDERS",
        "Surfing"                       : "WATER - WONDERS",
        "Water Rafting"                 : "WATER - WONDERS"
}

for k, v in TAGS.iteritems():
    if Tag.objects(Q(name=k) & Q(category=v)):
        continue
    Tag(name=k, category=v).save()
    print Tag.objects(Q(name=k) & Q(category=v))

print "Tags: ", len(Tag.objects.all())

