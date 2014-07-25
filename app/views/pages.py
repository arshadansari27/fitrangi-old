from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from mongoengine import Q

from app.models import *



class ListView(MethodView):

    def get(self):
        url_prefix = self.getUrlPrefix()
        categories = {}
        post_type = self.getType()
        posts = []
        if post_type.name in ['ORGANISER', 'DEALER']:
            users = User.objects(user_type=post_type).all()
            for user in users:
                post = user.profile
                posts.append(post)
            url = 'user/list.html'
            categories = {post_type.name: posts}
            print post_type.name, posts
            return render_template(url, categories=categories, url_prefix=url_prefix)
        else:
            url = 'post/list.html'
            posts = Post.objects(post_type=post_type).all()
            for post in posts:
                for t in post.tags:
                    categories.setdefault(t.name, [])
                    categories[t.name].append(post)
            return render_template(url, categories=categories, url_prefix=url_prefix)

class DetailView(MethodView):

    def get(self, key):
        url_prefix = self.getUrlPrefix()
        comment_type = PostType.objects(name__iexact='COMMENT').first()
        post_type = self.getType()
        if post_type.name in ['ORGANISER', 'DEALER']:
            post_type2 = self.getType2()
            post= Post.objects(post_type=post_type2).get_or_404(pk=key)
        else:
            post = Post.objects(post_type=post_type).get_or_404(pk=key)
        comments = Post.objects(Q(post_type=comment_type) & Q(parent=post)).all()
        return render_template('post/detail.html', post=post, comments=comments, url_prefix=url_prefix)


class ActivityView(object):
    def getType(self): 
        return PostType.objects(name__iexact='ACTIVITY').first() 

    def getUrlPrefix(self):
        return 'activities'

class DestinationView(object):
    def getType(self): 
        return PostType.objects(name__iexact='DESTINATION').first() 

    def getUrlPrefix(self):
        return 'destinations'

class EventView(object):
    def getType(self): 
        return PostType.objects(name__iexact='EVENT').first() 

    def getUrlPrefix(self):
        return 'events'

class OrganiserView(object):
    def getType(self): 
        return UserType.objects(name__iexact='ORGANISER').first()

    def getType2(self):
        return PostType.objects(name__iexact='PROFILE').first() 

    def getUrlPrefix(self):
        return 'organisers'

class DealerView(object):
    def getType(self): 
        return UserType.objects(name__iexact='DEALER').first()

    def getType2(self):
        return PostType.objects(name__iexact='PROFILE').first() 

    def getUrlPrefix(self):
        return 'dealers'

class ArticleView(object):

    def getType(self): 
        return PostType.objects(name__iexact='ARTICLE').first() 

    def getUrlPrefix(self):
        return 'articles'

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
class ArticleListView(ListView, ArticleView): pass
class ArticleDetailView(DetailView, ArticleView): pass

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

articles = Blueprint('articles', __name__, template_folder='templates')
articles.add_url_rule('/articles/', view_func=ArticleListView.as_view('list'))
articles.add_url_rule('/articles/<key>/', view_func=ArticleDetailView.as_view('detail'))
