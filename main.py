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

  ## make this so its always unique by referring to a set or using md5 or something
  theID = str(random.randint(1,9999)).zfill(4) + "-" + str(random.randint(1,9999)).zfill(4) + "-" + str(random.randint(1,9999)).zfill(4) + "-" + str(random.randint(1,9999)).zfill(4)
  return theID

#################### NDB Models #######################
#######################################################

class Pixel(ndb.Model):
  img = ndb.BlobKeyProperty()

##################### Web handlers  ###################
#######################################################

class MainPage(webapp2.RequestHandler):
    """Get a URL, POST a GA hit"""

    def get(self):

        template_values = {}

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

class LandingPage(webapp2.RequestHandler):
  """Example page where content is - utm parameters should be used plus cid which will link the impression and visit """

  def get(self):

        cid   = cgi.escape(self.request.get('cid'))
        clientId = getUniqueClientId(cid)

        print clientId
      
        template_values = {'clientId' : clientId}

        template = JINJA_ENVIRONMENT.get_template('landing-page.html')
        self.response.write(template.render(template_values))

class ImageRequest(blobstore_handlers.BlobstoreDownloadHandler):
  """The image that is in the email, and has a unique ID attached to it"""
  """This is called when the image is viewed, say in an email or another website"""

  def get(self):
        p      = cgi.escape(self.request.get('p'))
        c      = cgi.escape(self.request.get('c'))
        cid    = cgi.escape(self.request.get('cid'))
        nohit = cgi.escape(self.request.get('nohit'))

        ## if it has the same seed, creates an id like xxxx-xxxx-xxxx-xxxx
        cid = getUniqueClientId(cid)

        ## construct the Measurement Protocol call
        ga_url_stem = "http://www.google-analytics.com/collect"

        ## refer to https://developers.google.com/analytics/devguides/collection/protocol/v1/devguide
        values = {'v'   : 1,
                  'tid' : 'UA-54019251-3', ## replace with your GA ID
                  'cid' : cid}
        if p:  ## make a pageview when people see the image
          values['t']  = 'pageview'
          values['dh'] = 'external_email'
          values['ec'] = 'email'
          values['ea'] = 'open'

        else: ## else make an event
          values['t']  = 'event'
          values['ec'] = 'email'
          values['ea'] = 'open'

        if c: ## put campaign info in the pageview
          values['el'] = c
          values['dp'] = '/vpv/email-view/' + c
        else: ## put campaign info in the event labels
          values['el'] = "campaign_name"
          values['dp'] = '/vpv/email-view'
        ### z is the cache buster
        values['z'] = str(random.randint(1,999999)).zfill(6)

        if not nohit: ## nohit=1 if you don't want to send hit to GA
          ### send the hit to Google as a POST
          data = urllib.urlencode(values)
          req = urllib2.Request(ga_url_stem, data)
          response = urllib2.urlopen(req)
          the_page = response.read()

        print values  ## look in logs to see what was sent 

        ### get the image upload previously done at /upload-image.html and stored in datastore
        pixel = Pixel.get_by_id("image")

        ### serve up image
        if pixel:
          img = blobstore.BlobInfo.get(pixel.img)
          self.send_blob(img)
        else:
          self.response.out.write("no image")


class uploadPixel(webapp2.RequestHandler):
  """Upload an image handler used in the /upload-image form"""
  def get(self):
        upload_url = blobstore.create_upload_url('/upload-image2')
        template_values = {'upload_url' : upload_url }

        template = JINJA_ENVIRONMENT.get_template('upload-image.html')
        self.response.write(template.render(template_values))

class BlobStoreHandler(blobstore_handlers.BlobstoreUploadHandler):
  """ get the image upload to datastore, called on submit of /upload-image form"""
  def post(self):
        image   = self.get_uploads('img')
        blob_info = image[0]
        print blob_info

        pixel = Pixel(id="image")
        pixel.img = blob_info.key()
        pixel.put()

        self.redirect('/main.html')


application = ndb.toplevel(webapp2.WSGIApplication([
    ('/', MainPage),
    ('/main.png', ImageRequest),
    ('/landing-page', LandingPage),
    ('/upload-image', uploadPixel),
    ('/upload-image2',BlobStoreHandler)
], debug=True))
