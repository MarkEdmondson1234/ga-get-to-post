import fix_path
import urllib
import urllib2

from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import jinja2
import webapp2
import os
import datetime
import cgi
import json
import random


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#################### Functions #######################
#######################################################

def getUniqueClientId(seed=''):

  if seed: random.seed(seed)

  ## make this so its always unique by referring to a set
  theID = str(random.randint(1,9999)).zfill(4) + "-" + str(random.randint(1,9999)).zfill(4) + "-" + str(random.randint(1,9999)).zfill(4) + "-" + str(random.randint(1,9999)).zfill(4)
  return theID

#################### NDB Models #######################
#######################################################

class Pixel(ndb.Model):
  img = ndb.BlobKeyProperty()

##################### Web handlers  ###################
#######################################################

class uploadPixel(webapp2.RequestHandler):

  """Upload an image """
  def get(self):
        upload_url = blobstore.create_upload_url('/upload-image2')
        template_values = {'upload_url' : upload_url }

        template = JINJA_ENVIRONMENT.get_template('upload-image.html')
        self.response.write(template.render(template_values))

class BlobStoreHandler(blobstore_handlers.BlobstoreUploadHandler):
  """ get the image upload to datastore """
  def post(self):
        image   = self.get_uploads('img')
        blob_info = image[0]
        print blob_info

        pixel = Pixel(id="image")
        pixel.img = blob_info.key()
        pixel.put()

        self.redirect('/upload-image')

class LandingPage(webapp2.RequestHandler):
  """Example page where content is - utm parameters shoudl be used plus cid which will link the impression and visit """

  def get(self):

        cid   = cgi.escape(self.request.get('cid'))
        clientId = getUniqueClientId(cid)
      
        template_values = {'clientId' : clientId}

        template = JINJA_ENVIRONMENT.get_template('landing-page.html')
        self.response.write(template.render(template_values))

class ImageRequest(blobstore_handlers.BlobstoreDownloadHandler):
  """The image that is in the email, and has a unique ID attached to it"""

  def get(self):
        v   = cgi.escape(self.request.get('v'))
        tid = cgi.escape(self.request.get('tid'))
        cid = cgi.escape(self.request.get('cid'))
        t   = cgi.escape(self.request.get('t'))
        ec  = cgi.escape(self.request.get('ec'))
        ea  = cgi.escape(self.request.get('ea'))
        el  = cgi.escape(self.request.get('el'))
        cs  = cgi.escape(self.request.get('cs'))
        cm  = cgi.escape(self.request.get('cm'))
        cn  = cgi.escape(self.request.get('cn'))

        ## if it has the same seed, creates an id like xxxx-xxxx-xxxx-xxxx
        cid = getUniqueClientId(cid)

        ## construct the Measurement Protocol call
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
                  'cn'  : cn,
                  ### z is the cache buster
                  'z'   : str(random.randint(1,999999)).zfill(6) }

        ### send the hit to Google
        data = urllib.urlencode(values)
        req = urllib2.Request(ga_url_stem, data)
        response = urllib2.urlopen(req)
        the_page = response.read()

        ### get the image upload previously done at /form.html and stored in datastore
        pixel = Pixel.get_by_id("image")

        ### serve up image
        if pixel:
          img = blobstore.BlobInfo.get(pixel.img)
          # self.response.headers['Content-Type'] = 'image/png'
          # self.response.out.write(img)
          self.send_blob(img)
        else:
          self.response.out.write("no image")


class MainPage(webapp2.RequestHandler):
    """Get a URL, POST a GA hit"""

    def get(self):

        v   = cgi.escape(self.request.get('v'))
        tid = cgi.escape(self.request.get('tid'))
        cid = cgi.escape(self.request.get('cid'))
        t   = cgi.escape(self.request.get('t'))
        ec  = cgi.escape(self.request.get('ec'))
        ea  = cgi.escape(self.request.get('ea'))
        el  = cgi.escape(self.request.get('el'))
        cs  = cgi.escape(self.request.get('cs'))
        cm  = cgi.escape(self.request.get('cm'))
        cn  = cgi.escape(self.request.get('cn'))

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
           'data': data
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


application = ndb.toplevel(webapp2.WSGIApplication([
    ('/', MainPage),
    ('/main.png', ImageRequest),
    ('/landing-page', LandingPage),
    ('/upload-image', uploadPixel),
    ('/upload-image2',BlobStoreHandler)
], debug=True))
