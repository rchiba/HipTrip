from config import config

from xml.etree import ElementTree
import time
from xml.dom.minidom import parseString
import webapp2
from pymongo import Connection    
import re

from math import radians, cos, sin, asin, sqrt
      
class HeatmapHandler(webapp2.RequestHandler):

    def __init__(self, request=None, response=None):
        # as described here: http://stackoverflow.com/questions/8488482/attributeerror-nonetype-object-has-no-attribute-route-and-webapp2/8488737#8488737
        self.initialize(request, response)
        connection = Connection()
        db = connection['tweetsDB']
        self.tweets = db.tweetsCollection

        self.tweetUsers = db.tweetUsersCollection
        self.poiHeatmapCount = 100 # ? how many tweets to inspect for the heatmap
        
        db = connection['flickrDB']
        self.flickr = db.flickrCollection
        
        db = connection['linkedDB']
        self.linked = db.linkedCollection
        
        db = connection['yelpDB']
        self.yelp = db.yelpCollection
        
          
    # used in calculating hipness score
    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        return km 
          
    def getFlickrHeatmap(self, place = 'san francisco'):
        start = time.clock()

        resData = "{ \"max\":1, \"data\":["
        for photo in self.flickr.find({"place":place}):
            lat = photo['loc'][0]
            lon = photo['loc'][1]
            resData = '%s {"lat": %s, "lon": %s, "count": 1},' % (resData, lat, lon)
        if resData.endswith(","):resData = resData[:-1] #remove the trailing comma
        resData = resData+"]}"
        
        elapsed = (time.clock() - start)   
        print "getFlickrHeatmap finished in %s seconds" % elapsed
        self.response.write(resData)
        
        
    # gets the twitter heatmap using either mongo or sleepycat dbtype
    def getTwitterHeatmap(self, place = 'san francisco'):
        print 'place is %s'%place
        start = time.clock()
        resData = "{ \"max\":1, \"data\":["
        for tweet in self.tweets.find({"place":place}):
            lat = tweet['loc'][0]
            lon = tweet['loc'][1]
            resData = '%s {"lat": %s, "lon": %s, "count": 1},' % (resData, lat, lon)
        if resData.endswith(","):resData = resData[:-1] #remove the trailing comma
        resData = resData+"]}"
        elapsed = (time.clock() - start)
        print "getTwitterHeatmap finished in %s seconds" % elapsed
        self.response.write(resData)
        
    #deprecated
    def getLocalsHeatmap(self, place = 'san francisco'):
        start = time.clock()
        resData = "{ \"max\":1, \"data\":["
        for tweet in self.tweets.find({"place":place}):
            #print tweet['fromUserID']
            if tweet['fromUserID'] is not None:
                tweetUser = self.tweetUsers.find_one({'id':tweet['fromUserID']})
                if tweetUser is not None:
                    tweetUserLocation = tweetUser['location']
                    if tweetUserLocation is not None:
                        tweetUserLocation = tweetUserLocation.encode('utf-8')
                        #print tweetUserLocation
            if(tweetUserLocation is not None and 'san francisco' in tweetUserLocation.lower()):
                #print '%s is apparently a local' % tweetUserLocation
                lat = tweet['loc'][0]
                lon = tweet['loc'][1]
                resData = '%s {"lat": %s, "lon": %s, "count": 1},' % (resData, lat, lon)
        for photo in self.flickr.find({"place":place, "ownerLocation":re.compile('san francisco', re.IGNORECASE)}):
            #print 'photo ownerLocation:%s is a local' % photo['ownerLocation']
            lat = photo['loc'][0]
            lon = photo['loc'][1]
            resData = '%s {"lat": %s, "lon": %s, "count": 1},' % (resData, lat, lon)
        if resData.endswith(","):resData = resData[:-1] #remove the trailing comma
        resData = resData+"]}"
        elapsed = (time.clock() - start)
        print "getLocalsHeatmap finished in %s seconds" % elapsed
        self.response.write(resData)
    
    # returns the heatmap for a given poi
    # which consists of nearby tweet geo's
    # weighted by their user's distance from poi
    # ex: /yelpID/heatmap/poi
    def getPoiHeatmap(self, place):
        start = time.clock()
        resData = "{ \"max\":3, \"data\":["
        yelpEntry = self.yelp.find_one({"id":place})
        loc = yelpEntry["loc"]

        nearTweets = self.tweets.find({"loc":{"$near":loc}}).limit(self.poiHeatmapCount)
        nearTweetUserLocations = []
        for tweet in nearTweets:
            tweetUserID = tweet["fromUserID"]
            # get tweet user's data
            tweetUser = self.tweetUsers.find_one({"id":tweetUserID})
            if tweetUser is not None:
                if tweetUser.get("loc") is not None: 
                    # we're only heatmapping tweets with a user with a location
                    userLat = tweet['loc'][0] # we use the tweet's geo
                    userLon = tweet['loc'][1]
                    dist = self.haversine(userLat,userLon,loc[0],loc[1])
                    if dist < config['localDistance']: # locals
                        score = 3
                    elif dist < config['semiLocalDistance']: # semi - locals
                        score = 2
                    else: # tourists
                        score = 1
                    resData = '%s {"lat": %s, "lon": %s, "count": %s},' % (resData, userLat, userLon, score)
    
        if resData.endswith(","):resData = resData[:-1] #remove the trailing comma
        resData = resData+"]}"
        elapsed = (time.clock() - start)
        print "getPoiHeatmap finished in %s seconds" % elapsed
        self.response.write(resData)
    
    # deprecated
    def getTouristsHeatmap(self, place = 'san francisco'):
        start = time.clock()
        resData = "{ \"max\":1, \"data\":["
        for tweet in self.tweets.find({"place":place}):
            #print tweet['fromUserID']
            if tweet['fromUserID'] is not None:
                tweetUser = self.tweetUsers.find_one({'id':tweet['fromUserID']})
                if tweetUser is not None:
                    tweetUserLocation = tweetUser['location']
                    if tweetUserLocation is not None:
                        tweetUserLocation = tweetUserLocation.encode('utf-8')
                        #print tweetUserLocation
            if(tweetUserLocation is not None and not 'san francisco' in tweetUserLocation.lower()):
                #print '%s is apparently a tourist' % tweetUserLocation
                lat = tweet['loc'][0]
                lon = tweet['loc'][1]
                resData = '%s {"lat": %s, "lon": %s, "count": 1},' % (resData, lat, lon)
        for photo in self.flickr.find({"place":place, "ownerLocation":{"$not":re.compile('san francisco', re.IGNORECASE)}}):
            lat = photo['loc'][0]
            lon = photo['loc'][1]
            resData = '%s {"lat": %s, "lon": %s, "count": 1},' % (resData, lat, lon)
        if resData.endswith(","): resData = resData[:-1] #remove the trailing comma
        resData = resData+"]}"
        elapsed = (time.clock() - start)
        print "getTouristsHeatmap finished in %s seconds" % elapsed
        self.response.write(resData)
        
    def get(self, place, type):
        # return a list of JSON coordinates based on logic located here
        # where are the tourists and where are the locals?
        print "HeatmapHandler(self, "+place+", "+type+")"
        #print "Tuples in graph: %s" % len(self.graph)
        
        #translate shortened place to place as used throughout this webapp
        if place == 'sf':
            place = 'san francisco'
        elif place == 'la':
            place = 'los angeles'
        elif place == 'greece':
            place = 'greece'
        else: # place is a poi
            place = place
        
        if type == "flickr":
            self.getFlickrHeatmap(place)
        elif type == "twitter":
            self.getTwitterHeatmap(place)
        elif type == "locals":
            self.getLocalsHeatmap(place)
        elif type == "tourists":
            self.getTouristsHeatmap(place)
        elif type == "poi":
            self.getPoiHeatmap(place)