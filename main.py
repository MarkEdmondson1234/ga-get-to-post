import fix_path
import urllib
import urllib2

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
import os
import datetime
import cgi
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    """Get a URL, POST a GA hit"""

    def get(self):

        v = cgi.escape(self.request.get('v'))
        tid = cgi.escape(self.request.get('tid'))
        cid = cgi.escape(self.request.get('cid'))
        t = cgi.escape(self.request.get('t'))
        ec = cgi.escape(self.request.get('ec'))
        ea = cgi.escape(self.request.get('ea'))
        el = cgi.escape(self.request.get('el'))
        cs = cgi.escape(self.request.get('cs'))
        cm = cgi.escape(self.request.get('cm'))
        cn = cgi.escape(self.request.get('cn'))

        ga_url_stem = "http://www.google-analytics.com/collect"

        values = {'v'   : v,
                  'tid' : tid,
                  'cid' : cid,
                  't'   : t,
                  'ec'  : ec,
                  'ea'  : ea,
                  'el'  : el,
                  'cs'  : cs,
                  'cm'  : cm,
                  'cn'  : cn }

        data = urllib.urlencode(values)
        req = urllib2.Request(ga_url_stem, data)
        response = urllib2.urlopen(req)
        the_page = response.read()

        print data, req, response, the_page


        template_values = {
           'data': data,
           'output':response.read()
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):

        template_values = {
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


application = ndb.toplevel(webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True))
