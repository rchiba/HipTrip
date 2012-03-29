from config import config
from xml.etree import ElementTree
import time
from xml.dom.minidom import parseString
import webapp2
from pymongo import Connection, json_util
import json
import re

     
class poiHandler(webapp2.RequestHandler):

    def __init__(self, request=None, response=None):
        # as described here: http://stackoverflow.com/questions/8488482/attributeerror-nonetype-object-has-no-attribute-route-and-webapp2/8488737#8488737
        self.initialize(request, response)
        connection = Connection()
        
        db = connection['tweetsDB']
        self.tweets = db.tweetsCollection
        self.tweetUsers = db.tweetUsersCollection
        
        db = connection['flickrDB']
        self.flickr = db.flickrCollection
        
        db = connection['linkedDB']
        self.linked = db.linkedCollection
        
        db = connection['yelpDB']
        self.yelp = db.yelpCollection
        
        self.mostLinkedCount = 20 # how many most linked pois to return?
        self.nearbyTweetCount = 10 # how many nearby tweets to return?
        self.nearbyFlickrCount = 10 # how many nearby photos to return?
        
    # returns the most linked points of interest in the given place
    def getMostLinked(self, place = 'san francisco'):
        
        start = time.clock()

        resData = "["
        # find all distinct yelpID's and then order by its count
        pois = {}
        for poi in self.linked.distinct("yelpID"):
            count = self.linked.find({"yelpID":poi}).count()
            pois[poi] = count # store id and count in dict
        
        #sort dict
        pois = sorted(pois.iteritems(), key=lambda (k,v): (v,k), reverse=True)
        count = 0 
        for key, value in pois:
            #print value
            #generate json from sorted dict
            yelpEntry = self.yelp.find_one({"id":key})
            yelpJson = json.dumps(yelpEntry, default=json_util.default)
            resData = '%s %s,' % (resData, yelpJson)    
            count = count + 1
            if count > self.mostLinkedCount:
                break
        if resData.endswith(","):resData = resData[:-1] #remove the trailing comma
        
        resData = "%s ]" % resData
        
        elapsed = (time.clock() - start)   
        print "getMostLinked finished in %s seconds" % elapsed
        self.response.write(resData)
        
    # Returns a json with details to be displayed about a given POI
    # Called whenever a marker is clicked
    # place - the yelpid
    # ex: /yelpid/poi/details
    # I'll find...
    # - linked tweets
    # - linked flickr photos
    # - nearby tweets
    # - nearby flickr photos
    # - hipness score
    # - yelp review snippets
    def getDetails(self, place):
        start = time.clock()
        resData = "[" # we're returning an array of objects 
        # (each object being the raw entity mongo entry in json format)
        
        # - linked tweets and linked flickr photos
        linkedData = self.linked.find({"yelpID":place})
        for item in linkedData:
            if item.get("tweetID") is not None:
                tweetEntry = self.tweets.find_one({"id":item["tweetID"]})
                if tweetEntry is not None:
                    tweetEntry["type"] = "linkedTweet"
                    tweetEntry = json.dumps(tweetEntry, default=json_util.default)
                    resData = '%s %s,' % (resData, tweetEntry)   
            elif item.get("flickrID") is not None:
                flickrEntry = self.flickr.find_one({"id":item["flickrID"]})
                if flickrEntry is not None:
                    flickrEntry["type"] = "linkedFlickr"
                    flickrEntry = json.dumps(flickrEntry, default=json_util.default)
                    resData = '%s %s,' % (resData, flickrEntry)   
        
        # - nearby tweets and nearby flickr photos
        yelpEntry = self.yelp.find_one({"id":place})
        loc = yelpEntry["loc"]
        nearTweets = self.tweets.find({"loc":{"$near":loc}}).limit(self.nearbyTweetCount)
        for tweet in nearTweets:
            tweet["type"] = "nearbyTweet"
            tweet = json.dumps(tweet, default=json_util.default)
            resData = '%s %s,' % (resData, tweet)  
        nearFlickr = self.tweets.find({"loc":{"$near":loc}}).limit(self.nearbyFlickrCount)
        for flickr in nearFlickr:
            flickr["type"] = "nearbyFlickr"
            flickr = json.dumps(flickr, default=json_util.default)
            resData = '%s %s,' % (resData, flickr)  

        # - yelp review snippets
        yelpEntries = self.yelp.find({"id":place})
        for yelp in yelpEntries:
            yelp["type"] = "yelpEntry"
            yelp = json.dumps(yelp, default=json_util.default)
            resData = '%s %s,' % (resData, yelp)  
        
        # - hipness score : TODO
        
        
        if resData.endswith(","):resData = resData[:-1] #remove the trailing comma
        elapsed = (time.clock() - start)   
        print "getDetails() finished in %s seconds" % elapsed
        
        
        resData = "%s ]" % resData
        self.response.write(resData)
    
        
    def get(self, place, type):
        # return a list of JSON coordinates based on logic located here
        # where are the tourists and where are the locals?
        print "poiHandler(self, "+place+", "+type+")"
        #print "Tuples in graph: %s" % len(self.graph)
        
        #translate shortened place to place as used throughout this webapp
        if place == 'sf':
            place = 'san francisco'
        elif place == 'la':
            place = 'los angeles'
        elif place == 'greece':
            place = 'greece'
        
        if type == "mostlinked":
            self.getMostLinked(place)
        elif type == "details":
            self.getDetails(place)