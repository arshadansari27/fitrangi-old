from flask import Blueprint, request, redirect, render_template, url_for, abort
from flask.views import MethodView
from app.models import Node
from config import configuration
import datetime

url_prefixes = {}
for k, v in configuration['views'].iteritems():
    url_prefix = v['url-prefix']
    url_prefixes[url_prefix] = {'name': k, 'page-types': v['page-types']}

class ListView(MethodView):

    def get(self, url_prefix):
        global url_prefixes
        categories = {}
        prefix_data = url_prefixes.get(url_prefix, None)
        if prefix_data is None:
            raise Exception("Unknown problem with,%s" % url_prefix)
        _types = prefix_data['page-types']
        query = {'type': {"$in": _types}}

        nodes = Node.find(query) 
        count = Node.find_count(query) 
        print nodes
        print count
        # Assert that all _types belong to same template structure
        templates = configuration['templates']
        template = None
        for k, v in templates.iteritems():
            if all(_t in (pg_type for pg_type in v['page-types']) for _t in _types):
                template = k
                break
        if template is None:
            raise Exception("No template found for _types: %s" % str(_types))
        
         
        url = template + '/list.html'
        for p in nodes:
            for t in p.tags:
                categories.setdefault(t, [])
                categories[t].append(p)

        return render_template(url, categories=categories, url_prefix=url_prefix)

class DetailView(MethodView):

    def get(self, url_prefix, key):

        node = Node.get_by_id(key)
        if not node:
            abort(404)
        _type = node.type
        templates = configuration['templates']
        template = None
        for k, v in templates.iteritems():
            if _type in v['page-types']:
                template = k
                break
        if template is None:
            raise Exception("No template found for _types: %s" % str(_types))
         
        url = template + '/detail.html'
        
        comments = list(Node.find({'type': 'Comment', 'belongs_to': str(node._id)}))
        print '*** All Comments', comments
        return render_template(url, node=node, allcomments=comments, url_prefix=url_prefix)

blueprints = []
for k_view in configuration['views'].keys():
    view = Blueprint(k_view, __name__, template_folder='templates')
    view.add_url_rule('/view/<url_prefix>', view_func=ListView.as_view('list'))
    view.add_url_rule('/view/<url_prefix>/<key>/', view_func=DetailView.as_view('detail'))
    blueprints.append(view)
