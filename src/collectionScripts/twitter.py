import rdflib
from xml.etree import ElementTree

from rdflib.graph import Graph
from rdflib import Literal, BNode, Namespace
from rdflib import RDF
from rdflib.graph import ConjunctiveGraph as Graph
from rdflib import plugin
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib.namespace import Namespace
from rdflib.term import Literal
from rdflib.term import URIRef
from tempfile import mkdtemp

from xml.dom.minidom import parseString
import tweepy
from tweepy import Cursor

import time

rdflib.plugin.register('MySQL', Store,'rdfstorage.MySQL', 'MySQL')

default_graph_uri = "http://example.com/rdfstore"

configString = "host=localhost,user=root,password=,db=rdfstore"

# Get the mysql plugin. You may have to install the python mysql libraries                                                                                                         
store = plugin.get('MySQL', Store)('rdfstore')
# Open previously created store, or create it if it doesn't exist yet
# Open previously created store, or create it if it doesn't exist yet
rt = store.open(configString,create=False)
if rt == 0:
    # There is no underlying MySQL infrastructure, create it
    store.open(configString,create=True)
else:
    assert rt == VALID_STORE,"There underlying store is corrupted"   
                                                                                                           
g = Graph(store, identifier = URIRef(default_graph_uri))


g.bind("dc", "http://purl.org/dc/elements/1.1/")
dcURL = "http://purl.org/dc/elements/1.1/"
DC = Namespace(dcURL)

GEO = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
g.bind("geo", "http://www.w3.org/2003/01/geo/wgs84_pos#")

FOAF = Namespace('http://xmlns.com/foaf/0.1/')
g.bind("foaf", "http://xmlns.com/foaf/0.1/")

custom = Namespace('http://localhost/')
g.bind("custom", "http://localhost/")

#setup sparql
plugin.register(
    'sparql', rdflib.query.Processor,
    'rdfextras.sparql.processor', 'Processor')
plugin.register(
    'sparql', rdflib.query.Result,
    'rdfextras.sparql.query', 'SPARQLQueryResult')
        
        
        
        
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
print "Twitter collection script running under %s with %s queries left. Limit resets at %s." % (api.me().name, api.rate_limit_status()['remaining_hits'], time.ctime(api.rate_limit_status()['reset_time_in_seconds']))


def storeTweetsFor(place):
    if place == 'san francisco':
        geo = '37.758,-122.442,7km'
    elif place == 'los angeles':
        geo = ' '
    elif place == 'greece':
        geo = ' '
        
    counter = 0
    for tweet in Cursor(api.search, q='', geocode=geo, rpp=100).items(1500):
        #print '%s %s %s' % (tweet.id, tweet.from_user, tweet.geo)
        counter += 1
        
        #only store tweets with geocode
        if tweet.geo is not None:
            lat=float(tweet.geo['coordinates'][0])
            lon=float(tweet.geo['coordinates'][1])
            createdAt=tweet.created_at
            id=str(tweet.id)
            text=tweet.text
            fromUser=tweet.from_user
            fromUserID=str(tweet.from_user_id)
            
            print '%s: %s tweeted, %s, at %s: %s %s' % (counter, fromUser, text.encode('utf-8'), createdAt, lat, lon)
            
            # store tweet in local store
            g.add((custom[id], RDF.type, custom["Tweet"]))
            g.add((custom[id], DC["Identifier"], Literal(id)))
            g.add((custom[id], DC["Creator"],  custom[fromUserID]))
            g.add((custom[id], DC["dateSubmitted"],  Literal(createdAt)))
            g.add((custom[id], DC["Description"],  Literal(text)))
            g.add((custom[id], GEO['lat'], Literal(lat)))
            g.add((custom[id], GEO['lon'], Literal(lon)))
            
            # store owner in local store
            g.add((custom[fromUserID], RDF.type,  FOAF['Person']))
            g.add((custom[fromUserID], custom['username'], Literal(fromUser)))
        
storeTweetsFor('san francisco')
        
        
