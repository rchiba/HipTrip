from config import config

import time
from xml.dom.minidom import parseString
import webapp2
from pymongo import Connection    
import re
from cluster import KMeansClustering
        
class ClustersHandler(webapp2.RequestHandler):

    def __init__(self, request=None, response=None):
        # as described here: http://stackoverflow.com/questions/8488482/attributeerror-nonetype-object-has-no-attribute-route-and-webapp2/8488737#8488737
        self.initialize(request, response)
        connection = Connection()
        db = connection['tweetsDB']
        self.tweets = db.tweetsCollection
        #print '%s entries in tweetsCollection' % self.tweets.count()
        self.tweetUsers = db.tweetUsersCollection
        #print '%s entries in tweetUsersCollection' % self.tweetUsers.count()
        self.clusterNum = 10
        
        db = connection['flickrDB']
        self.flickr = db.flickrCollection
        #print '%s entries in flickrCollection' % self.flickr.count()
                           
    def getFlickrClusters(self, place = 'san francisco'):
        start = time.clock()

        
        clusterData = []
        for photo in self.flickr.find({"place":place}):
            lat = photo['loc'][0]
            lon = photo['loc'][1]
            clusterData.append((lat,lon))
        
        cl = KMeansClustering(clusterData)
        clusters = cl.getclusters(self.clusterNum)
        elapsed = (time.clock() - start)   
        print "getFlickrCluster finished in %s seconds" % elapsed
        
        #only return center of clusters
        resData = "["
        for cluster in clusters:
            latTotal = 0
            lonTotal = 0
            for point in cluster:
                latTotal += point[0]
                lonTotal += point[1]
            centerLat = latTotal/len(cluster)
            centerLon = lonTotal/len(cluster)
            resData = "%s(%s,%s)," % (resData, centerLat, centerLon)
        if resData.endswith(","):resData = resData[:-1] #remove the trailing comma
        resData = "%s]"%resData
        
        self.response.write(resData)
        
        
    # gets the twitter heatmap using either mongo or sleepycat dbtype
    def getTwitterClusters(self, place = 'san francisco'):
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
        
    def getLocalsClusters(self, place = 'san francisco'):
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
        
    def getTouristsClusters(self, place = 'san francisco'):
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
        print "ClustersHandler(self, "+place+", "+type+")"
        #print "Tuples in graph: %s" % len(self.graph)
        
        #translate shortened place to place as used throughout this webapp
        if place == 'sf':
            place = 'san francisco'
        elif place == 'la':
            place = 'los angeles'
        elif place == 'greece':
            place = 'greece'
        
        if type == "flickr":
            self.getFlickrClusters(place)
        elif type == "twitter":
            self.getTwitterClusters(place)
        elif type == "locals":
            self.getLocalsClusters(place)
        elif type == "tourists":
            self.getTouristsClusters(place)