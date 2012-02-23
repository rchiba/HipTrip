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


# rdflib.plugin.register('MySQL', Store,'rdfstorage.MySQL', 'MySQL')

# default_graph_uri = "http://example.com/rdfstore"

# configString = "host=localhost,user=root,password=,db=rdfstore"

#Get the mysql plugin. You may have to install the python mysql libraries                                                                                                         
# store = plugin.get('MySQL', Store)('rdfstore')
#Open previously created store, or create it if it doesn't exist yet
#Open previously created store, or create it if it doesn't exist yet
# rt = store.open(configString,create=False)
# if rt == 0:
  #  There is no underlying MySQL infrastructure, create it
    # store.open(configString,create=True)
# else:
    # assert rt == VALID_STORE,"There underlying store is corrupted"   
                                                                                                           
# g = Graph(store, identifier = URIRef(default_graph_uri))


# g.bind("dc", "http://purl.org/dc/elements/1.1/")
# dcURL = "http://purl.org/dc/elements/1.1/"
# DC = Namespace(dcURL)

# GEO = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
# g.bind("geo", "http://www.w3.org/2003/01/geo/wgs84_pos#")

# FOAF = Namespace('http://xmlns.com/foaf/0.1/')
# g.bind("foaf", "http://xmlns.com/foaf/0.1/")

# custom = Namespace('http://localhost/')
# g.bind("custom", "http://localhost/")

#setup sparql
# plugin.register(
    # 'sparql', rdflib.query.Processor,
    # 'rdfextras.sparql.processor', 'Processor')
# plugin.register(
    # 'sparql', rdflib.query.Result,
    # 'rdfextras.sparql.query', 'SPARQLQueryResult')
        


        
class HeatmapHandler(webapp2.RequestHandler):

    def __init__(self, request=None, response=None):
        # as described here: http://stackoverflow.com/questions/8488482/attributeerror-nonetype-object-has-no-attribute-route-and-webapp2/8488737#8488737
        self.initialize(request, response)
        
        
        # sleepycat initialization
        if not config['enableMongo']:
            default_graph_uri = "http://example.com/rdfstore"
            config_string = "collectionScripts/rdfstore"
            # Register plugins
            plugin.register("sparql", Processor, "rdfextras.sparql.processor", "Processor")
            plugin.register("sparql", Result, "rdfextras.sparql.query", "SPARQLQueryResult")
            
            store = plugin.get("Sleepycat", Store)("collectionScripts/rdfstore")
            rt = store.open(config_string, create=False)
            if rt == NO_STORE:
                store.open(config_string, create=True)
            else:
                assert rt == VALID_STORE, "The underlying store is corrupted" 
            
            self.graph = Graph(store, identifier=URIRef(default_graph_uri))
            self.graph.bind("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
            self.graph.bind("dc", "http://purl.org/dc/elements/1.1/")
            self.graph.bind("geo", "http://www.w3.org/2003/01/geo/wgs84_pos#")
            self.graph.bind("foaf", "http://xmlns.com/foaf/0.1/")
            self.graph.bind("custom", "http://localhost")
            
            self.namespaces = { "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
                           "dc":Namespace("http://purl.org/dc/elements/1.1/"),
                           "geo":Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#"),
                           "foaf":Namespace("http://xmlns.com/foaf/0.1/"),
                               "custom":Namespace("http://localhost/")}

        if config['enableMongo']: # I wonder how we should use mongo for faster storage, or if we should at all...
            connection = Connection()
            db = connection['tweetsDB']
            self.tweets = db.tweetsCollection
            print '%s entries in tweetCollection' % self.tweets.count()
                           
    def getFlickrHeatmap(self):
    
        # get each flickr photo, lat, lon, and owner's based_near
        #heatmapQuery
        # heatmapQuery = g.query(
        # """SELECT ?photoID ?lat ?lon ?ownerLocation
           # WHERE {
              # ?photoURI rdf:type dc:Image .
              # ?photoURI dc:Identifier ?photoID . 
              # ?photoURI geo:lat ?lat .
              # ?photoURI geo:lon ?lon .
              # ?photoURI dc:Creator ?ownerURI .
              # ?ownerURI foaf:based_near ?ownerLocation .
           # }""",
        # initNs=dict(
            # dc=DC,
            # rdf=RDF,
            # geo=GEO,
            # foaf=FOAF))
     
        start = time.clock()
        heatmapQuery = self.graph.query(
        """SELECT ?photoURI ?lat ?lon
           WHERE {
              ?photoURI rdf:type dc:Image .
              ?photoURI geo:lat ?lat .
              ?photoURI geo:lon ?lon .
           }""",
        initNs=self.namespaces)
        elapsed = (time.clock() - start)   
        print "Query finished in %s seconds" % elapsed
        resData = self.returnJSONHeatmap(heatmapQuery.result)
        print "All done! \n"
        self.response.write(resData)
        
    # used to iter through sparql query results
    def returnJSONHeatmap(self,queryResult):
        start = time.clock()
        resData = "{ \"max\":1, \"data\":["
        
        for idx, row in enumerate(queryResult):
            # get photo details and store them
            #if idx>1000: break
            
            lat = row[1]
            lon = row[2]
            resData = resData+"{\"lat\": "+lat+", \"lon\": "+lon+", \"count\": 1},"
            #print(row)
            #print(str(idx)+" out of "+str(len(heatmapQuery.result)))
            
        resData = resData[:-1] #remove the trailing comma
        resData = resData+"]}"
        elapsed = (time.clock() - start)
        print "Iteration finished in %s seconds" % elapsed
        return resData
        
    # gets the twitter heatmap using either mongo or sleepycat dbtype
    def getTwitterHeatmap(self, dbType = 'sleepycat'):
        print "getTwitterHeatmap"
        if dbType == 'sleepycat':
            start = time.clock()
            twitterQuery = self.graph.query(
                """SELECT ?x ?lat ?lon ?text
                   WHERE {
                      ?x rdf:type "tweet".
                      ?x geo:lat ?lat .
                      ?x geo:lon ?lon .
                   }""",
                initNs=self.namespaces)
            elapsed = (time.clock() - start)
            print "Query finished in %s seconds" % elapsed
            resData = self.returnJSONHeatmap(twitterQuery.result)
            print "All done! \n"
            self.response.write(resData)
        elif dbType == 'mongo':
            start = time.clock()
            resData = "{ \"max\":1, \"data\":["
            for tweet in self.tweets.find():
                lat = tweet['lat']
                lon = tweet['lon']
                resData = '%s {"lat": %s, "lon": %s, "count": 1},' % (resData, lat, lon)
            resData = resData[:-1] #remove the trailing comma
            resData = resData+"]}"
            elapsed = (time.clock() - start)
            print "Iteration finished in %s seconds" % elapsed
            self.response.write(resData)
        
    def get(self, location, type):
        # return a list of JSON coordinates based on logic located here
        # where are the tourists and where are the locals?
        print "HeatmapHandler(self, "+location+", "+type+")"
        #print "Tuples in graph: %s" % len(self.graph)
        if type == "flickr":
            self.getFlickrHeatmap()
        elif type == "twitter":
            self.getTwitterHeatmap('sleepycat')
        elif type == "twitterMongo":
            self.getTwitterHeatmap('mongo')
    