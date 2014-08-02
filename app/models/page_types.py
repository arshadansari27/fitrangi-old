import datetime
from types import Node

def get_attributes_for(page_type):
    print page_type
    found = PAGE_TYPES.get(page_type, None)
    if not found:
        return None
    attributes = set([])
    _attributes = found.get('attributes', [])
    if len(_attributes) > 0:
        for v in _attributes:
            attributes.add(v)
    while found.get('parent', None) is not None:
        print found['parent']
        found = PAGE_TYPES.get(found['parent'], None)
        if not found:
            break
        _attributes = found.get('attributes', [])
        if len(_attributes) > 0:
            for v in _attributes:
                attributes.add(v)
    return attributes


PAGE_TYPES = {
    'Node': {
        'parent': None,
        'attributes': [tuple(['created_on', datetime.datetime, None, None])]
    },
    'Post': {
        'parent': 'Node',
        'attributes': [
            ('images', str, None, list), ('videos', str, None, list), ('created_by', Node, 'Profile', None), 
            ('title', str, None, None), ('text', str, None, None), ('published_on', datetime.datetime, None, None), 
            ('is_published', bool, None, None), ('type', str, None, None), ('tags', str, None, list), ('page_access', str, None, None),
            ('related', Node, 'Post', list)]
    },
    'Profile': {
        'parent': 'Node', 
        'attributes': [
            ('name', str, None, None), ('email', str, None, None), ('phone', str, None, None), ('address', str, None, None), ('website', str, None, None),
            ('facebook', str, None, None), ('linkedin', str, None, None), ('username', str, None, None), ('password', str, None, None),
            ('is_verified', bool, None, None), ('type', str, None, None), ('tags', str, None, list), 
            ('following', Node, 'Profile', list), ('followers', Node, 'Profile', list)]
    },
    'EventOrganiser': {
        'parent': 'Profile',
        'attributes': [
            ('events', Node, 'Post', list), ('advertisements', Node, 'Post', list)
        ]
    },
    'Retailer': {
        'parent': 'Profile',
        'attributes': [
            ('products', Node, 'Post', list), ('advertisements', Node, 'Post', list)
        ]
    },
    'Enthusiast': {
        'parent': 'Profile',
        'attributes': [('blogs', Node, 'Post', list), ('comments', Node, 'Post', list), ('questions', Node, 'Post', list)]

    },
    'Admin': {
        'parent': 'Profile'
    },
    'Professional': {
        'parent': 'Profile'
    },
    'Blog': {
        'parent': 'Post'
    },
    'Query': {
        'parent': 'Post'
    },
    'Comment': {
        'parent': 'Post',
        'attribute': [('belongs_to', Node, 'Post', None), ('reply_to', Node, 'Post', None)]
    },
    'Advertisement': {
        'parent': 'Post',
        'attribute': [tuple([('ad_for', Node, 'Post', None)])]
    },
    'Event': {
        'parent': 'Post',
        'attributes': [('from', datetime.datetime, None, None), ('to', datetime.datetime, None, None), ('event_organiser', Node, 'Profile', None)]
    },
    'Product': {
        'parent': 'Post',
        'attributes': [('price', float, None, None), ('discount', float, None, None), ('retailer', Node, 'Profile', None)]
    },
    'Activity': {
        'parent': 'Post'
    },
    'Destination': {
        'parent': 'Post',
    },
    'FitrangiSpecial': {
        'parent': 'Post'
    },
    'Trip': {
        'parent': 'Event'
    },
    'Gathering': {
        'parent': 'Event'
    },
    'Trainer': {
        'parent': 'Professional'
    },
    'Guide': {
        'parent': 'Professional'
    },
    'Rescuer': {
        'parent': 'Professional'
    },
    'Clothes': {
        'parent': 'Product'
    },
    'Footwear': {
        'parent': 'Product'
    },
    'Accessories': {
        'parent': 'Product'
    },
    'Tools': {
        'parent': 'Product'
    },
    "Sky - Fly": {
        'parent': 'Activity'
    },
    "Snow - Flow":{
        'parent': 'Activity'
    },  
    "Travelling & Sightseeing":{
        'parent': 'Activity'
    },  
    "Water - Wonders": {
        'parent': 'Activity'
    },  
    "Land Sports": {
        'parent': 'Activity'
    },  
    "Other Sports": {
        'parent': 'Activity'
    },  
    "Camping": {
        'parent': 'Land Sports'
    },                       
    "Cycling-Biking": {
        'parent': 'Land Sports'
    },
    "Marathons": {
        'parent': 'Land Sports'
    },       
    "Mountaineering": {
        'parent': 'Land Sports'
    }, 
    "Off-beat Activities": {
        'parent': 'Land Sports'
    },
    "Rappelling & Valley Crossing": {
        'parent': 'Land Sports'
    },   
    "Rock Climbing": {
        'parent': 'Land Sports'
    },
    "Trekking & Hiking": {
        'parent': 'Land Sports'
    },
    "Horse Riding": {
        'parent': 'Other Sports'
    },
    "Stargazing": {
        'parent': 'Other Sports'
    }, 
    "Zorbing": {
        'parent': 'Other Sports'
    }, 
    "Bungee jumping": {
        'parent': 'Sky - Fly'
    },
    "Hang Gliding": {
        'parent': 'Sky - Fly'
    },
    "Hot Air Ballooning": {
        'parent': 'Sky - Fly'
    },
    "Para Motoring": {
        'parent': 'Sky - Fly'
    },
    "Paragliding": {
        'parent': 'Sky - Fly'
    },
    "Parasailing": {
        'parent': 'Sky - Fly'
    },
    "Sky Diving": {
        'parent': 'Sky - Fly'
    },
    "Zip Line": {
        'parent': 'Sky - Fly'
    },
    "Architecture Monuments": {
        'parent': "Travelling & Sightseeing"
    },
    "Beaches": {
        'parent': "Travelling & Sightseeing"
    },
    "Forts & Caves": {
        'parent': "Travelling & Sightseeing"
    },
    "Hill stations": {
        'parent': "Travelling & Sightseeing"
    },
    "Places to Visit": {
        'parent': "Travelling & Sightseeing"
    },
    "Theme Parks": {
        'parent': "Travelling & Sightseeing"
    },
    "Wildlife Sanctuaries & Safaris": {
        'parent': "Travelling & Sightseeing"
    },
    "Canyoning":{
        'parent': "Water - Wonders"
    },
    "Kayaking": {
        'parent': "Water - Wonders"
    },
    "Kite Surfing": {
        'parent': "Water - Wonders"
    },
    "Scuba Diving": {
        'parent': "Water - Wonders"
    },
    "Snorkelling": {
        'parent': "Water - Wonders"
    },
    "Surfing": {
        'parent': "Water - Wonders"
    },
    "Water Rafting": {
        'parent': "Water - Wonders"
    },
    "Export": {
        'parent': 'FitrangiSpecial'
    },
    "Informative": {
        'parent': 'FitrangiSpecial'
    },
    "Top 5 Series": {
        'parent': 'FitrangiSpecial'
    }
}


