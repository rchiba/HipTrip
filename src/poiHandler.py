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
        
    # returns the most linked points of interest in the given place
    def getMostLinked(self, place = 'san francisco'):
        returnedValues = 15 #return only this many number of values
    
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
            print value
            #generate json from sorted dict
            yelpEntry = self.yelp.find_one({"id":key})
            yelpJson = json.dumps(yelpEntry, default=json_util.default)
            resData = '%s %s,' % (resData, yelpJson)    
            count = count + 1
            if count > returnedValues:
                break
        if resData.endswith(","):resData = resData[:-1] #remove the trailing comma
        
        resData = resData+"]"
        
        elapsed = (time.clock() - start)   
        print "getMostLinked finished in %s seconds" % elapsed
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