'''
Created on Feb 22, 2012

@author: rchiba
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
from pymongo import Connection

class TwitterDataScraper():
    def __init__(self, type):
    
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
        self.counter = 100 # a way to limit our queries - set to -1 if we want to collect indefinitely
        self.maxTweetsPerQuery = 1500 # as defined by twitter
        self.maxRPP = 100 # as defined by twitter
        self.hitsLeftBeforeExit = 200 # calls to search api do not count to this limit
        self.untilDate = '2012-02-18' #the day after the day we would like to collect
        self.calmTimeout = 30 # seconds to wait when rate limited
        self.oldestID = 0 # store oldestID so we can figure out next iteration's max_id (max_id is inclusive)
        self.geo = '' # a string used in search api for location

        #these are used in querying twitter
        self.locations = {"san francisco":'37.758,-122.442,7km',
                            "los angeles": "",
                            "greece": ""}
                            
        print "Twitter collection script running with %s queries left. Limit resets at %s." % (self.api.rate_limit_status()['remaining_hits'], time.ctime(self.api.rate_limit_status()['reset_time_in_seconds']))
        
        if type=="sleepycat":
            # sleepycat initialization
            default_graph_uri = "http://example.com/rdfstore"
            config_string = "rdfstore"
            # Register plugins
            plugin.register("sparql", Processor, "rdfextras.sparql.processor", "Processor")
            plugin.register("sparql", Result, "rdfextras.sparql.query", "SPARQLQueryResult")
            
            store = plugin.get("Sleepycat", Store)("rdfstore")
            rt = store.open(config_string, create=False)
            if rt == NO_STORE:
                store.open(config_string, create=True)
            else:
                assert rt == VALID_STORE, "The underlying store is corrupted" 
            
            self.graph = Graph(store, identifier=URIRef(default_graph_uri))
            self.graph.bind("dc", "http://purl.org/dc/elements/1.1/")
            self.graph.bind("geo", "http://www.w3.org/2003/01/geo/wgs84_pos#")
            self.graph.bind("foaf", "http://xmlns.com/foaf/0.1/")
            self.graph.bind("custom", "http://localhost")
            
            self.namespaces = {"dc":Namespace("http://purl.org/dc/elements/1.1/"),
                               "geo":Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#"),
                           "foaf":Namespace("http://xmlns.com/foaf/0.1/"),
                           "custom":Namespace("http://localhost/")}
                           
            self.twitter_url = "http://www.twitter.com/%s"
        elif type=="mongo":
            connection = Connection()
            db = connection['tweetsDB']
            self.collection = db.tweetsCollection
        

    # wrapper function for recursive solution to finding tweets
    def storeTweetsFor(self, place):
        self.geo = self.locations[place]
            
        #ryo - last id was 169843803547639808
        self.recursivelyStoreTweets(self.geo, self.untilDate, '169843803547639808')
        
        
    def recursivelyStoreTweets(self, geo, untilDate, maxID):
        self.oldestID = maxID
        try:
            for tweet in Cursor(self.api.search, q='', until=self.untilDate, geocode=geo, rpp=self.maxRPP, max_id=maxID).items(self.maxTweetsPerQuery-1000): #-1000 since otherwise I get invalid query errors if a query returns less than this number of items
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
                   
                    if type == "mongo": #store in mongo
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
                        self.collection.update(key, tweet, True);
                    
                    elif type == "sleepycat": #store in sleepycat
                        self.graph.add((URIRef(self.twitter_url % id), self.namespaces["rdf"]["type"], Literal("tweet")))
                        self.graph.add((URIRef(self.twitter_url % id), self.namespaces["dc"]["identifier"], Literal(id)))
                        self.graph.add((URIRef(self.twitter_url % id), self.namespaces["dc"]["dateSubmitted"], Literal(createdAt)))
                        self.graph.add((URIRef(self.twitter_url % id), self.namespaces["dc"]["creator"], Literal(fromUserID)))
                        self.graph.add((URIRef(self.twitter_url % id), self.namespaces["geo"]["lat"], Literal(lat)))
                        self.graph.add((URIRef(self.twitter_url % id), self.namespaces["geo"]["lon"], Literal(lon)))
                        self.graph.add((URIRef(self.twitter_url % id), self.namespaces["dc"]["description"], Literal(text)))
                        
                    
                #else:
                #   print '%s: %s tweeted at %s' % (tweet.id, tweet.from_user, tweet.created_at)

                
            # if we are almost out of queries, stop, else continue
            if self.api.rate_limit_status()['remaining_hits'] > self.hitsLeftBeforeExit and (self.counter == -1 or self.counter > 0):
                self.counter = self.counter - 1
                # recurse
                print '%s hits left... recursing again' % (self.api.rate_limit_status()['remaining_hits'])
                self.recursivelyStoreTweets(geo, untilDate, oldestID)
            else:
                # do nothing - exit case
                print 'Queries finished.'
                
        # handler for the continuous rate limiting
        except tweepy.error.TweepError as (err):
            print err
            if (str(err).find('calm') != -1):
                #rate limited, so wait awhile and then restart
                print 'rated limited... enhancing calm for %s seconds' % (calmTimeout)
                time.sleep(calmTimeout)
                recursivelyStoreTweets(geo, untilDate, oldestID)
                
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

                
def main():
    x = TwitterDataScraper("mongo")
    x.storeTweetsFor("san francisco")
    print "Tuples in graph: %s" % len(x.graph)
    x.query_store()
        
if __name__ == "__main__":
    main()     
        
