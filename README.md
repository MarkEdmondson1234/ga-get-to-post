Universal Analytics image to click tracking
===========================================

Call me a GET png with the correct parameters and you get a POST to your GA account.

Clone this project or see a demo live here: http://ua-post-to-push.appspot.com/ 

This is a demo of how you can use Google Analytics to track opens of an email using an image that when loads, triggers a hit to GA, and then be able to link that image hit with a later session that clicks through to view and possibly convert.

Applications include email tracking and affiliate sales tracking.

## To use:

* Upload an image you would like to appear. This can be any .png, including a 1x1 pixel.
* Construct the URL for the event you would like to track. 
* If you use p=1, it will record opens under '/vpv/email-view/' (+ campaign from c if present).  This lets you use it in GA funnels.
* c=campaign name, which will record in the pageview or event label
* If you use nohit=1, it will not record an email view (used for displaying the image without triggering a GA hit)
* The cid parameter will construct the anonymous ID for GA to link sessions together. It can be text or a number. An email address works - example: cid=mark.edmondson@example.com
* Once you have constructed the URL, use it as where the image is loaded from. It has to "hotlink" the image, if it loads via a CDN it won't work (e.g. if you load the image into Twitter, Facebook etc. they save it on their own servers

Example Image URL with event data with cid=blah, virtual pageviews (p=1) and email_campaign for the open (recorded as an event label)

```
http://your-appengine-id.appspot.com/main.png?cid=blah&p=1&c=email_campaign
```

* Every view of that image URL will result in a hit in GA. Send it in an email, or put it on an affiliates thank you page.  In a live project, make the parameters dynamic based on what you would like to record.
* To link sessions, the landing page should be setup to accept the cid. An example of the GA javascript needed <a href="http://ua-post-to-push.appspot.com/landing-page">is available here</a>
* Any links in the email (or the image) that land on the landing page with the same cid as above (e.g. cid=mark.edmondson@example.com) will be linked to the image view session. Put utm_campaign etc. parameters on there as well if you like

- Example full click URL with campaign parameters and cid = "blah"

```
http://your-appengine-id.appspot.com/landing-page?cid=blah&utm_source=source_me&utm_medium=medium_me&utm_campaign=campaign_me
```


## Example URLs

- Example Image URL with cid=blah, virtual pageviews (p=1) and email_campaign for the open recorded as /vpv/email-view/email_campaign

```
http://your-appengine-id.appspot.com/main.png?cid=blah&p=1&c=email_campaign
```

- Example URL for links within the email for same user, cid=blah

```
http://your-appengine-id.appspot.com/landing-page?cid=blah + utm parameters
```

- Example full click URL with campaign parameters and cid

```
http://your-appengine-id.appspot.com/landing-page?cid=blah&utm_source=source_me&utm_medium=medium_me&utm_campaign=campaign_me
```

