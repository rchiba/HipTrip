from config import config

import rdflib
from xml.etree import ElementTree

from rdflib.graph import Graph
from rdflib import Literal, BNode, Namespace
from rdflib import RDF
from rdflib.graph import ConjunctiveGraph as Graph
from rdflib import plugin
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib.query import Processor, Result
from rdflib.namespace import Namespace
from rdflib.term import Literal
from rdflib.term import URIRef
from tempfile import mkdtemp
import time
from xml.dom.minidom import parseString
import webapp2
from pymongo import Connection    
import re

        
class HeatmapHandler(webapp2.RequestHandler):

    def __init__(self, request=None, response=None):
        # as described here: http://stackoverflow.com/questions/8488482/attributeerror-nonetype-object-has-no-attribute-route-and-webapp2/8488737#8488737
        self.initialize(request, response)
        connection = Connection()
        db = connection['tweetsDB']
        self.tweets = db.tweetsCollection
        #print '%s entries in tweetsCollection' % self.tweets.count()
        self.tweetUsers = db.tweetUsersCollection
        #print '%s entries in tweetUsersCollection' % self.tweetUsers.count()
        
        
        db = connection['flickrDB']
        self.flickr = db.flickrCollection
        #print '%s entries in flickrCollection' % self.flickr.count()
                           
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
        
        if type == "flickr":
            self.getFlickrHeatmap(place)
        elif type == "twitter":
            self.getTwitterHeatmap(place)
        elif type == "locals":
            self.getLocalsHeatmap(place)
        elif type == "tourists":
            self.getTouristsHeatmap(place)