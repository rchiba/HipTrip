'''
Created on Mar 28, 2012

@author: rchiba
'''

from pymongo import Connection, GEO2D
from nltk.metrics import edit_distance
import yql
import sys

class LocalTouristClassifier():
    def __init__(self):
        self.tweets = Connection().tweetsDB.tweetsCollection
        self.tweetUsers = Connection().tweetsDB.tweetUsersCollection
        self.tweetUsers.ensure_index( [("loc", GEO2D )] )
        
        self.photos = Connection().flickrDB.flickrCollection
        self.linked = Connection().linkedDB.linkedCollection
        self.MAX_EDIT_DISTANCE = 3
        self.places = ['san francisco','los angeles']
        self.place = self.places[0] # a tourist or local of where?
        self.cityEditDistanceThreshold = 2
        API_KEY = 'dj0yJmk9UUY5TWxNMXBRb0M3JmQ9WVdrOVV6RlVOWFEzTjJzbWNHbzlNVGMzTVRBNE5EazJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD0zYQ--'
        SHARED_SECRET = '92a96753c369996f18b6a2ef4a6b1b9c85de04f5'
        self.y = yql.TwoLegged(API_KEY, SHARED_SECRET)
        self.yqlCache = {}
        
    def unescape_html_chars(self, item):
        return item.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").replace("&quot;", "\"")
        
    def isLocalOf(self, userLocation, place):
        if place is self.places[0]: # san francisco
            # split by comma, whitespace, trim, then exact match for SF or threshold for san francisco
            userLocation = userLocation.lower().strip()
            userLocation = userLocation.split(',');
            for token in userLocation:
                token.strip()
                if edit_distance(token, 'san francisco') < self.cityEditDistanceThreshold:
                    return True
                if edit_distance(token, 'san francisco ca') < self.cityEditDistanceThreshold:
                    return True
                if 'san francisco' in token:
                    return True
                elif token is 'sf':
                    return True
                    
            return False
        
    def classifyTwitter(self):
        for tweet in self.tweets.find({"place":self.place}):
            if tweet['fromUserID'] is not None:
                tweetUser = self.tweetUsers.find_one({'id':tweet['fromUserID']})
                if tweetUser is not None:
                    tweetUserLocation = tweetUser['location']
                    if tweetUserLocation is not None and tweetUser['loc'] is None:
                        tweetUserLocation = tweetUserLocation.encode('utf-8')
                        #print "%s || %s" % (tweetUserLocation, self.place)
                        # we use the yqlCache local dictionary to use as few calls as possible
                        if self.yqlCache.get(tweetUserLocation) is not None and self.yqlCache[tweetUserLocation] != 0:
                            tweetUser['loc'] = self.yqlCache[tweetUserLocation]
                            print 'cacheSuccess: %20s %15s %s' % (tweetUserLocation, tweetUser['id'], tweetUser['loc'])
                        else:
                            # send request out to YQL
                            yqlQuery = 'select * from geo.placefinder where text="%s";' % tweetUserLocation
                            try:
                                yqlResult = self.y.execute(yqlQuery)
                                if yqlResult.rows == []:
                                    # yql couldn't figure out where this is, so don't save a loc
                                    self.yqlCache[tweetUserLocation] = 0
                                    print 'fail: %20s %s' % (tweetUserLocation, tweetUser['id'])
                                else:
                                    # yql found a lat and lon, so let's tag it
                                    loc = [float(yqlResult.rows[0].get('latitude')), float(yqlResult.rows[0].get('longitude'))]
                                    tweetUser['loc'] = loc
                                    self.yqlCache[tweetUserLocation] = loc
                                    print 'success: %20s %15s %s' % (tweetUserLocation, tweetUser['id'], loc)
                            except:
                                print "Exception Detected:", sys.exc_info()[0]
                                
                        # ready to save user
                        self.tweetUsers.save(tweetUser)
                        # if(tweetUserLocation is not None and self.isLocalOf(tweetUserLocation, self.place)):
                            # #user is a local, so store this info
                            # tweetUser['localOf'] = self.place
                            # self.tweetUsers.save(tweetUser)
                            # print "Local  : %15s %s" % (tweetUserLocation, tweetUser['id'])
                        # else:
                            # print "Tourist: %15s %s" % (tweetUserLocation, tweetUser['id'])
                            
                            
def main():
    print "Beginning Twitter user classification"
    
    l = LocalTouristClassifier()
    l.classifyTwitter()
    
    print "Finished Twitter user classification"
if __name__=="__main__":
    main()