from config import config
from xml.etree import ElementTree
import time
from xml.dom.minidom import parseString
import webapp2
from pymongo import Connection, json_util
import json
import re
import random
from nltk import word_tokenize
from math import radians, cos, sin, asin, sqrt
     
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
        self.nearbyTweetCount = 100 # how many nearby tweets to return?
        self.nearbyFlickrCount = 30 # how many nearby photos to return?
        
        
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
        
        yelpEntry = self.yelp.find_one({"id":place})
        loc = yelpEntry["loc"]
        
        # - linked tweets and linked flickr photos
        linkedData = self.linked.find({"yelpID":place})
        for item in linkedData:
            if item.get("tweetID") is not None:
                tweetEntry = self.tweets.find_one({"id":item["tweetID"]})
                if tweetEntry is not None:
                    tweetEntry["type"] = "linkedTweet"
                    tweetUserID = tweetEntry["fromUserID"]
                    # get tweet user's data
                    tweetUser = self.tweetUsers.find_one({"id":tweetUserID})
                    if tweetUser is not None:
                        if tweetUser.get("loc") is not None: #store dist for heatmap generation
                            # nearTweetUserLocations.append(tweetUser["loc"]) # using this for hipness calc
                            tweetUser["dist"] = self.haversine(tweetUser["loc"][0],tweetUser["loc"][1],loc[0],loc[1])
                        tweetUser["type"] = "nearbyTweetUser"
                        tweetUserEntry = json.dumps(tweetUser, default=json_util.default)
                        tweetEntry["userdata"] = json.JSONDecoder().decode(tweetUserEntry)
                    tweetEntry = json.dumps(tweetEntry, default=json_util.default)
                    resData = '%s %s,' % (resData, tweetEntry)    
                    
            elif item.get("flickrID") is not None:
                flickrEntry = self.flickr.find_one({"id":item["flickrID"]})
                if flickrEntry is not None:
                    flickrEntry["type"] = "linkedFlickr"
                    flickrEntry = json.dumps(flickrEntry, default=json_util.default)
                    resData = '%s %s,' % (resData, flickrEntry)   
        
        # - nearby tweets and nearby flickr photos
        nearTweets = self.tweets.find({"loc":{"$near":loc}}).limit(self.nearbyTweetCount)
        nearTweetUserLocations = []
        for tweet in nearTweets:
            tweet["type"] = "nearbyTweet"
            tweetUserID = tweet["fromUserID"]
            # get tweet user's data
            tweetUser = self.tweetUsers.find_one({"id":tweetUserID})
            if tweetUser is not None:
                if tweetUser.get("loc") is not None:
                    nearTweetUserLocations.append(tweetUser["loc"]) # using this for hipness calc
                    tweetUser["dist"] = self.haversine(tweetUser["loc"][0],tweetUser["loc"][1],loc[0],loc[1])
                tweetUser["type"] = "nearbyTweetUser"
                tweetUserEntry = json.dumps(tweetUser, default=json_util.default)
                tweet["userdata"] = json.JSONDecoder().decode(tweetUserEntry)
            tweet = json.dumps(tweet, default=json_util.default)
            resData = '%s %s,' % (resData, tweet)  
            
        nearFlickr = self.flickr.find({"loc":{"$near":loc}}).limit(self.nearbyFlickrCount)
        for flickr in nearFlickr:
            flickr["type"] = "nearbyFlickr"
            if flickr.get("userLoc") is not None:
                flickr["dist"] = self.haversine(flickr["userLoc"][0],flickr["userLoc"][1],loc[0],loc[1])
                print "flickr dist is %s"%flickr['dist']
            
            flickr = json.dumps(flickr, default=json_util.default)
            resData = '%s %s,' % (resData, flickr)  

        # - yelp review snippets
        yelpEntries = self.yelp.find({"id":place})
        for yelp in yelpEntries:
            yelp["type"] = "yelpEntry"
            yelp = json.dumps(yelp, default=json_util.default)
            resData = '%s %s,' % (resData, yelp)  
        
        avg = self.getHipnessScore(place)
        resData = '%s {"type":"hipness", "value":"%s"},' % (resData, avg*100) 
        
        
        if resData.endswith(","):resData = resData[:-1] #remove the trailing comma
        elapsed = (time.clock() - start)   
        print "getDetails() finished in %s seconds" % elapsed
        
        
        resData = "%s ]" % resData
        self.response.write(resData)
    
    # helper function for getting hipness score
    def confidence_fixed(ups, downs):
        if ups == 0:
            return -downs
        n = ups + downs
        z = 1.64485 #1.0 = 85%, 1.6 = 95%
        phat = float(ups) / n
        return (phat+z*z/(2*n)-z*sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
    
    # returns the hipness score given a yelp id (place)
    # we'll use the ranking algorithm discussed here
    # http://possiblywrong.wordpress.com/2011/06/05/reddits-comment-ranking-algorithm/
    def getHipnessScore(self, place):
        # - hipness score 
        # * find X closest tweets
        # * find how far away their users are tagged from POI
        # * score 100 - all locals, score 0 - all out of staters      
        # * factor in the yelp rating - which can be 0-5
        sum = 0.0
        yelpWeight = .3
        yelpEntry = self.yelp.find_one({"id":place})
        rating = yelpEntry["rating"]
        nearTweetUserLocCount = len(nearTweetUserLocations)
        for tweetLoc in nearTweetUserLocations:
            dist = self.haversine(tweetLoc[0],tweetLoc[1],loc[0],loc[1])
            if dist < config['localDistance']: # locals
                sum = sum + 1.0
            elif dist < config['semiLocalDistance']: # semi - locals
                sum = sum + .5
            else: # tourists
                sum = sum + 0
        
        sum = (nearTweetUserLocCount*yelpWeight) * (rating / 5) + sum
        nearTweetUserLocCount = nearTweetUserLocCount * (1+yelpWeight)
        
        
        avg = sum/nearTweetUserLocCount
        return avg
    
    
    
    # returns yelp pois when search bar is used
    # also returns some data for initial screen
    # like, we need to rank each poi before sending it down
    # relative to all the other finds
    # ex: /searchquery/poi/search
    def getSearch(self, query):
        start = time.clock()
        resData = "["
        query = query.lower()
        query = word_tokenize(query) # word tokens without stopwords
        yelpEntries = self.yelp.find({"_keywords":{"$in":query}})
        for yelpEntry in yelpEntries:
            if yelpEntry is not None:
                yelpJson = json.dumps(yelpEntry, default=json_util.default)
                resData = '%s %s,' % (resData, yelpJson)    

        if resData.endswith(","):resData = resData[:-1] #remove the trailing comma
        
        resData = "%s ]" % resData
        
        elapsed = (time.clock() - start)   
        print "getSearch finished in %s seconds" % elapsed
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
        elif type == "search":
            self.getSearch(place)