Universal Analytics image to click tracking
===========================================

Call me a GET png with the correct parameters and you get a POST to your GA account

This is a demo of how you can use Google Analytics to track opens of an email using an image that when loads, triggers a hit to GA, and then be able to link that image hit with a later session that clicks through to view and possibly convert.

Applications include email tracking and affiliate sales tracking.

## To use:

* Upload an image you would like to appear. This can be any .png, including a 1x1 pixel.
* Construct the URL for the event you would like to track. cid=uniqueId, if you include p=1 it will track as a virtual pageview (so be able to be used in GA funnels), c=campaign name
* If you use p=1, it will record opens under '/vpv/email-view/' (+ campaign from c if present)
* If you use nohit=1, it will not record an email view (used for displaying the image below without triggering a email view, for example)
* The cid parameter will construct the anonymous ID for GA to link sessions together. It can be text or a number. An email address works - example: cid=mark@wunderman.com
* Put that URL as where the image is loaded from. It has to "hotlink" the image, if it loads via a CDN it won't work (e.g. if you load the image into Twitter, Facebook etc. they save it on their own servers
* Every view of that image URL will result in a hit in GA. Send it in an email.
* To link sessions, the landing page should be setup to accept the cid. An example is available at this location
* Any links in the email (or the image) that land on the landing page with the same cid as above (e.g. cid=mark@edmondson.com) will be linked to the image view session. Put utm_campaign etc. parameters on there as well if you like

## Upload New Image

Example Image URL with event data with cid=blah, virtual pageviews (p=1) and email_campaign for the open (recorded as an event label)

http://gapost-wunderman.appspot.com/main.png?cid=blah&p=1&c=email_campaign
Example URL for links in the email for same user, cid=blah

http://gapost-wunderman.appspot.com/landing-page?cid=blah + utm parameters
....example full click URL

http://gapost-wunderman.appspot.com/landing-page?cid=blah&utm_source=source_me&utm_medium=medium_me&utm_campaign=campaign_me

