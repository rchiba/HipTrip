from tempfile import mkdtemp

from xml.dom.minidom import parseString
import tweepy
from tweepy import Cursor
from pymongo import Connection

import time


connection = Connection()
db = connection['tweetsDB']
collection = db.tweetsCollection

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="QwuBMbP2f9FQYoZBjF8fSA"
consumer_secret="Dvc4NEfSoYXdORxVRMdLkXkHMGO8PSxkkqL479XrFL4"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="8950292-DjfCvEpXTKbmb0TVZIP7XwAga2ua21LrFxglt0"
access_token_secret="DZX2rSmd6NpGUHXIJczq0OGYisBCFnQg6Dh6qu4oM"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# rate limit is 350 queries per hour, each search returning 100 tweets, max 1500 tweets per query, client side filtering for geo
maxTweetsPerQuery = 1500 # as defined by twitter
maxRPP = 100 # as defined by twitter
hitsLeftBeforeExit = 200 # we start out with 350 every hour, when our count hits this, then we no longer query
# all tweets collected for 2012-02-19
untilDate = '2012-02-18' #the day after the day we would like to collect
calmTimeout = 30 # seconds to wait when rate limited
global oldestID # store oldestID so we can figure out next iteration's max_id (max_id is inclusive)
global geo

print "Twitter collection script running with %s queries left. Limit resets at %s." % (api.rate_limit_status()['remaining_hits'], time.ctime(api.rate_limit_status()['reset_time_in_seconds']))


# wrapper function for recursive solution to finding tweets
def storeTweetsFor(place):
    if place == 'san francisco':
        geo = '37.758,-122.442,7km'
    elif place == 'los angeles':
        geo = ' '
    elif place == 'greece':
        geo = ' '
        
    #ryo - last id was 169843803547639808
    recursivelyStoreTweets(geo, untilDate, '169843803547639808')
        
        
def recursivelyStoreTweets(geo, untilDate, maxID):

    oldestID = maxID

    try:
        for tweet in Cursor(api.search, q='', until=untilDate, geocode=geo, rpp=maxRPP, max_id=maxID).items(maxTweetsPerQuery-1000): #-1000 since otherwise I get invalid query errors if a query returns less than this number of items
            oldestID = tweet.id
            #only store tweets with geocode
            if tweet.geo is not None:
                lat=float(tweet.geo['coordinates'][0])
                lon=float(tweet.geo['coordinates'][1])
                createdAt=tweet.created_at
                id=str(tweet.id)
                text=tweet.text
                fromUser=tweet.from_user
                fromUserID=str(tweet.from_user_id)
                
                print '%s: %16s tweeted at %s: %s %s' % (id, fromUser, createdAt, lat, lon)
               
                key = {"id": id}
                tweet = {
                    "id":id,
                    "createdAt": createdAt,
                    "fromUser": fromUser,
                    "lat": lat,
                    "lon": lon, 
                    "text": text, 
                    "fromUserID": fromUserID
                }
                
                # this should take care of duplicate insertions
                collection.update(key, tweet, True);
                
                #collection.insert(tweet)
                
            #else:
            #   print '%s: %s tweeted at %s' % (tweet.id, tweet.from_user, tweet.created_at)

            
        # if we are almost out of queries, stop, else continue
        if api.rate_limit_status()['remaining_hits'] > hitsLeftBeforeExit:
            # recurse
            print '%s hits left... recursing again' % (api.rate_limit_status()['remaining_hits'])
            recursivelyStoreTweets(geo, untilDate, oldestID)
        else:
            # do nothing
            print 'Queries finished.'
            
    except tweepy.error.TweepError as (err):
        print err
        if (str(err).find('calm') != -1):
            #rate limited, so wait awhile and then restart
            print 'rated limited... enhancing calm for %s seconds' % (calmTimeout)
            time.sleep(calmTimeout)
            recursivelyStoreTweets(geo, untilDate, oldestID)
        
#main
storeTweetsFor('san francisco')
        
        
