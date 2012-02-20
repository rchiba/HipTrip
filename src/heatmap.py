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
        

heatmapQuery = None
        
class HeatmapHandler(webapp2.RequestHandler):
    def get(self, location, type):
        # return a list of JSON coordinates based on logic located here
        # where are the tourists and where are the locals?
        print "HeatmapHandler(self, "+location+", "+type+")"
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
            
        global heatmapQuery
        if heatmapQuery is None:    
            heatmapQuery = g.query(
            """SELECT ?photoURI ?lat ?lon
               WHERE {
                  ?photoURI rdf:type dc:Image .
                  ?photoURI geo:lat ?lat .
                  ?photoURI geo:lon ?lon .
               }""",
            initNs=dict(
                dc=DC,
                rdf=RDF,
                geo=GEO,
                foaf=FOAF))
            
        print "Query finished"
        
        resData = "{ \"max\":1, \"data\":["
        
        for idx, row in enumerate(heatmapQuery.result):
            # get photo details and store them
            if idx>1000: break
            
            lat = row[1]
            lon = row[2]
            resData = resData+"{\"lat\": "+lat+", \"lon\": "+lon+", \"count\": 1},"
            #print(row)
            #print(str(idx)+" out of "+str(len(heatmapQuery.result)))
            
        resData = resData[:-1] #remove the trailing comma
        resData = resData+"]}"
        self.response.write(resData)

