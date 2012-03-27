'''
Created on Feb 22, 2012

@author: rchiba

Instructions
twitter.py [database type] [location or command]

Examples: 
'twitter.py sleepycat sf' - gathers tweets in sf and stores in sleepycat
'twitter.py mongo la' - gathers tweets in la and stores in mongo
'twitter.py sleepycat stats' - prints out stats of db
'''
from tempfile import mkdtemp
from xml.dom.minidom import parseString
import tweepy
from tweepy import Cursor
import time
from rdflib import Namespace, plugin
from rdflib.graph import Graph
from rdflib.query import Processor, Result
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib.term import Literal, URIRef
from json import loads
import oauth2
import urllib2
from pymongo import Connection, GEO2D
import sys

class TwitterDataScraper():
    def __init__(self):
    
        # twitter keys
        consumer_key="QwuBMbP2f9FQYoZBjF8fSA"
        consumer_secret="Dvc4NEfSoYXdORxVRMdLkXkHMGO8PSxkkqL479XrFL4"
        access_token="8950292-DjfCvEpXTKbmb0TVZIP7XwAga2ua21LrFxglt0"
        access_token_secret="DZX2rSmd6NpGUHXIJczq0OGYisBCFnQg6Dh6qu4oM"

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

        # local limits
        # rate limit is 350 queries per hour, each search returning 100 tweets, max 1500 tweets per query, client side filtering for geo
        self.counter = -1 # a way to limit our queries - set to -1 if we want to collect indefinitely
        self.maxTweetsPerQuery = 1500 # as defined by twitter
        self.maxRPP = 100 # as defined by twitter
        self.hitsLeftBeforeExit = 200 # calls to search api do not count to this limit
        self.untilDate = '2012-03-13' #the day after the day we would like to collect
        self.calmTimeout = 30 # seconds to wait when rate limited
        self.oldestID = 0 # store oldestID so we can figure out next iteration's max_id (max_id is inclusive)
        self.geo = '' # a string used in search api for location
        self.type = type
        #these are used in querying twitter
        self.locations = {"san francisco":'37.758,-122.442,7km',
                            "los angeles": "34.03,-118.33,20km",
                            "greece": ""}
        
        self.userDict = {} # used as a buffer to hold 100 users before we send out query for user info
        
        print "Twitter collection script running with %s queries left. Limit resets at %s." % (self.api.rate_limit_status()['remaining_hits'], time.ctime(self.api.rate_limit_status()['reset_time_in_seconds']))
        
        connection = Connection()
        db = connection['tweetsDB']
        self.tweetsCollection = db.tweetsCollection
        self.tweetsCollection.ensure_index( [("createdAt", 1 )] )
        self.tweetsCollection.ensure_index( [("loc", GEO2D )] )
        self.tweetsCollection.ensure_index( [("place", 1 )] )
        self.tweetUsersCollection = db.tweetUsersCollection
        self.tweetUsersCollection.ensure_index( [("id", 1 )] )
        
    # wrapper function for recursive solution to finding tweets
    def storeTweetsFor(self, place):
        self.geo = self.locations[place]
        self.place = place
        #ryo - last id was 169843803547639808
        self.recursivelyStoreTweets(self.geo, self.untilDate, '')
        
        
    def recursivelyStoreTweets(self, geo, untilDate, maxID):
        self.oldestID = maxID
        try:
            for tweet in Cursor(self.api.search, q='', until=self.untilDate, geocode=geo, rpp=self.maxRPP, max_id=maxID, with_twitter_user_id='true').items(self.maxTweetsPerQuery-1000): #-1000 since otherwise I get invalid query errors if a query returns less than this number of items
                self.oldestID = tweet.id
                #query api for details
                #only store tweets with geocode
                if tweet.geo is not None:
                    lat=float(tweet.geo['coordinates'][0])
                    lon=float(tweet.geo['coordinates'][1])
                    createdAt=tweet.created_at
                    id=str(tweet.id)
                    text=tweet.text
                    fromUser=tweet.from_user
                    fromUserID=tweet.from_user_id
                    if fromUserID not in self.userDict and self.tweetUsersCollection.find({'id':tweet.from_user_id}).count() == 0: # and not in users db already
                        #print 'adding %s to user buffer, len is %s and count is %s' % (fromUserID, len(self.userDict), self.tweetUsersCollection.find({'id':fromUserID}).count())
                        self.userDict[str(fromUserID)] = 'true'
                    
                    print '%s: %16s tweeted at %s: %s %s' % (id, fromUser, createdAt, lat, lon)
                   
                    key = {"id": id}
                    tweet = {
                        "id":id,
                        "createdAt": createdAt,
                        "fromUser": fromUser,
                        "loc": [lat,lon],
                        "text": text, 
                        "fromUserID": fromUserID,
                        "place": self.place
                    }
                    # this should take care of duplicate insertions
                    self.tweetsCollection.update(key, tweet, True)
                    
                    # if we've reached 100 usernames, make appropriate query
                    if len(self.userDict) == 99:
                        #print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!10 users buffered, time to store their info'
                        userQueryArr = []
                        for username in self.userDict.keys():
                            # make a query string of users
                            userQueryArr.append(username)
                        # get all the userInfo and store
                        #print userQueryArr
                        self.userDict = {} # empty out the buffer for next iters
                        for userInfo in self.api.lookup_users(user_ids=userQueryArr):
                            screenname = userInfo.screen_name.encode('utf-8')
                            name = userInfo.name.encode('utf-8')
                            location = userInfo.location
                            profileImgUrl = userInfo.profile_image_url
                            createdAt = userInfo.created_at
                            id = userInfo.id
                            followersCount = userInfo.followers_count
                            geoEnabled = userInfo.geo_enabled
                            tweetCount = userInfo.statuses_count
                            description = userInfo.description
                            #print 'id: %s and is of type %s' % (id, type(id))
                            if description is not None:
                                description = description.encode('utf-8')
                            userKey = {"id": id}
                            userValue = {
                                "id": id,
                                "location": location,
                                "profileImgUrl": profileImgUrl,
                                "createdAt": createdAt,
                                "followersCount": followersCount, 
                                "geoEnabled": geoEnabled,
                                "tweetCount": tweetCount,
                                "description": description,
                                "place": self.place
                            }
                            
                            self.tweetUsersCollection.update(userKey, userValue, True)
                            
                            #print 'user info successfully stored'
                
            # if we are almost out of queries, stop, else continue
            if self.api.rate_limit_status()['remaining_hits'] > self.hitsLeftBeforeExit and (self.counter != 0):
                self.counter = self.counter - 1
                # recurse
                print '%s hits left... recursing again' % (self.api.rate_limit_status()['remaining_hits'])
                self.recursivelyStoreTweets(geo, untilDate, self.oldestID)
            else:
                # do nothing - exit case
                print 'Queries finished.'
                
        # handler for the continuous rate limiting
        except tweepy.error.TweepError as (err):
            print err
            if (str(err).find('calm') != -1):
                #rate limited, so wait awhile and then restart
                print 'rated limited... enhancing calm for %s seconds' % (self.calmTimeout)
                time.sleep(self.calmTimeout)
                self.recursivelyStoreTweets(self.geo, self.untilDate, self.oldestID)
            elif (str(err).find('503') != -1):
                #rate limited, so wait awhile and then restart
                print 'service unavailable... trying again in %s seconds' % (self.calmTimeout)
                time.sleep(self.calmTimeout)
                self.recursivelyStoreTweets(self.geo, self.untilDate, self.oldestID)
                
    def query_store(self):
        # To iterate over all triples:
#        for (s,p,o) in self.graph.triples((None, None, None)):
#            print (s,p,o)
#        return

        # Query for a specific subject
        qres = self.graph.query("""
            SELECT DISTINCT ?p ?o
            WHERE {
                ?x ?p ?o
            }""", initNs=self.namespaces)
        
        for row in qres.result:
            print row
         
    def printTweetStats(self):
        print "Records in Tweets Collection: %s" % self.tweetsCollection.count()
        print "Records in Tweet Users Collection: %s" % self.tweetUsersCollection.count()
             
def main():

    if(len(sys.argv) == 1):
        print "Examples: 'twitter.py sf twitter.py la, twitter.py stats'"
        return

    
    
    type  = ''
    place = ''
    
            
    if (len(sys.argv) > 1):
        if( sys.argv[1] == 'sf' ):
            place = 'san francisco'
        elif(  sys.argv[1] == 'la' ):
            place = 'los angeles'
        elif( sys.argv[1] == 'stats' ):
            x = TwitterDataScraper()
            x.printTweetStats()
            return
        else:
            print 'invalid place type, use sf or la'
            return
    
    
    x = TwitterDataScraper()
    x.storeTweetsFor(place)
    
        
if __name__ == "__main__":
    main()     
        
