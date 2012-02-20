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
import webapp2

from pymongo import Connection

def twitterToText(storeType):
    lat = ''
    lon = ''
    time = ''
    text = ''
    if(storeType == 'rdflib'):
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

        CUSTOM = Namespace('http://localhost/')
        g.bind("custom", "http://localhost/")

        #setup sparql
        plugin.register(
            'sparql', rdflib.query.Processor,
            'rdfextras.sparql.processor', 'Processor')
        plugin.register(
            'sparql', rdflib.query.Result,
            'rdfextras.sparql.query', 'SPARQLQueryResult')
                
        f = open('tweets.txt', 'r+')

        # prints all tweets to a file
        print "twitterToText now printing all tweets to a file..."
            
        global tweetQuery
        tweetQuery = g.query(
        """SELECT ?tweetURI ?lat ?lon ?time ?text
           WHERE {
              ?tweets rdf:type custom:Tweet .
              GRAPH ?tweets {
                  ?tweetURI geo:lat ?lat .
                  ?tweetURI geo:lon ?lon .
                  ?tweetURI dc:dateSubmitted ?time .
                  ?tweetURI dc:Description ?text .
              }
           }
           LIMIT 5""",
        initNs=dict(
            dc=DC,
            rdf=RDF,
            geo=GEO,
            foaf=FOAF,
            custom=CUSTOM))
            
        #queries done, now print it
        for idx, row in enumerate(tweetQuery.result):
            # store all data in file
            if idx>1000: break #store only partial in file (for debugging purposes)
            #tweetURI = row[0]
            lat = row[1]
            lon = row[2]
            time = row[3]
            text = row[4]
            outputStr = "%s %s %s %s\n" % (lat, lon, time, text.encode('utf-8'))
            f.write(outputStr)

        print "Query finished"
        
    elif (storeType == 'mongo'):
        connection = Connection()
        db = connection['tweetsDB']
        collection = db.tweetsCollection

        resData = "["
        for tweet in collection.find():
            lat = tweet["lat"]
            lon = tweet["lon"]
            time = tweet["createdAt"]
            text = tweet["text"]
            resData += "{\"lat\": \"%s\", \"lon\": \"%s\", \"time\": \"%s\", \"text\": \"%s\"},\n" % (lat, lon, time, text.encode('utf-8').replace("\"","'").replace("\n",""))
            
        resData = resData[:-2] 
        resData += "]"
        f = open('tweets.txt', 'r+')
        f.write(resData) 
    
        
    
    
twitterToText('mongo') #set to either mongo or rdflib
print "twitterToText finished."

