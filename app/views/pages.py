from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from app.models import *



class ListView(MethodView):

    def get(self):
        url_prefix = self.getUrlPrefix()
        categories = set([])
        if issubclass(self.getClass(), User):
            users = self.getClass().objects.all()
            url = 'user/list.html'
            for a in users:
                categories.add(a.user_type)
            return render_template(url, categories=categories, users=users, url_prefix=url_prefix)
        elif  issubclass(self.getClass(), Post):
            posts = self.getClass().objects.all()
            url = 'post/list.html'
            for a in posts:
                categories.add(a.category)
            return render_template(url, categories=categories, posts=posts, url_prefix=url_prefix)
        else:
            raise Exception("Invalid class, not implemented")


class DetailView(MethodView):

    def get(self, key):
        url_prefix = self.getUrlPrefix()
        if issubclass(self.getClass(), User):
            user = self.getClass().objects.get_or_404(pk=key)
            profile = user.profile
            comments = Comment.objects(post=profile).all()
            return render_template('user/detail.html', user=user, profile=profile, comments=comments, url_prefix=url_prefix)
        elif  issubclass(self.getClass(), Post):
            post = self.getClass().objects.get_or_404(pk=key)
            comments = Comment.objects(post=post).all()
            return render_template('post/detail.html', post=post, comments=comments, url_prefix=url_prefix)
        else:
            raise Exception("Invalid class, not implemented")



class ActivityView(object):
    def getClass(self): 
        return Activity

    def getUrlPrefix(self):
        return 'activities'

class DestinationView(object):
    def getClass(self): 
        return Destination 

    def getUrlPrefix(self):
        return 'destinations'

class EventView(object):
    def getClass(self): 
        return Event

    def getUrlPrefix(self):
        return 'events'

class OrganiserView(object):
    def getClass(self): 
        return TripOrganiser

    def getUrlPrefix(self):
        return 'organisers'

class DealerView(object):
    def getClass(self): 
        return GearDealer

    def getUrlPrefix(self):
        return 'dealers'

class BlogView(object):
    def getClass(self):
        return Blog
    def getUrlPrefix(self):
        return 'blogs'

class ActivityListView(ListView, ActivityView): pass
class ActivityDetailView(DetailView, ActivityView): pass
class DestinationListView(ListView, DestinationView): pass
class DestinationDetailView(DetailView, DestinationView): pass
class EventListView(ListView, EventView): pass
class EventDetailView(DetailView, EventView): pass
class OrganiserListView(ListView, OrganiserView): pass
class OrganiserDetailView(DetailView, OrganiserView): pass
class DealerListView(ListView, DealerView): pass
class DealerDetailView(DetailView, DealerView): pass
class BlogListView(ListView, BlogView): pass
class BlogDetailView(DetailView, BlogView): pass

activities = Blueprint('activities', __name__, template_folder='templates')
activities.add_url_rule('/activities/', view_func=ActivityListView.as_view('list'))
activities.add_url_rule('/activities/<key>/', view_func=ActivityDetailView.as_view('detail'))

destinations = Blueprint('destinations', __name__, template_folder='templates')
destinations.add_url_rule('/destinations/', view_func=DestinationListView.as_view('list'))
destinations.add_url_rule('/destinations/<key>/', view_func=DestinationDetailView.as_view('detail'))

events = Blueprint('events', __name__, template_folder='templates')
events.add_url_rule('/events/', view_func=EventListView.as_view('list'))
events.add_url_rule('/events/<key>/', view_func=EventDetailView.as_view('detail'))

organisers = Blueprint('organisers', __name__, template_folder='templates')
organisers.add_url_rule('/organisers/', view_func=OrganiserListView.as_view('list'))
organisers.add_url_rule('/organisers/<key>/', view_func=OrganiserDetailView.as_view('detail'))

dealers = Blueprint('dealers', __name__, template_folder='templates')
dealers.add_url_rule('/dealers/', view_func=DealerListView.as_view('list'))
dealers.add_url_rule('/dealers/<key>/', view_func=DealerDetailView.as_view('detail'))

blogs = Blueprint('blogs', __name__, template_folder='templates')
blogs.add_url_rule('/blogs/', view_func=BlogListView.as_view('list'))
blogs.add_url_rule('/blogs/<key>/', view_func=BlogDetailView.as_view('detail'))
