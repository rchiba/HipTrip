import rdflib
import flickrapi

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

#setup store
# http://code.google.com/p/rdflib/w/list
# http://readthedocs.org/docs/rdflib/en/latest/persistence.html
# default_graph_uri = "http://localhost/rdfstore"
# store = plugin.get('Sleepycat', Store)('rdfstore')
#Open previously created store, or create it if it doesn't exist yet
# graph = Graph(store="Sleepycat",
              # identifier = URIRef(default_graph_uri))
# path = mkdtemp()
# rt = graph.open(path, create=False)
# if rt == NO_STORE:
#    There is no underlying Sleepycat infrastructure, create it
    # graph.open(path, create=True)
# else:
    # assert rt == VALID_STORE, "The underlying store is corrupt"

#setup graph
g=rdflib.Graph(store='Sleepycat')
g.open("rdfstore")
g.bind("dc", "http://purl.org/dc/elements/1.1/")
dcURL = "http://purl.org/dc/elements/1.1/"
DC = Namespace(dcURL)

#setup sparql
plugin.register(
    'sparql', rdflib.query.Processor,
    'rdfextras.sparql.processor', 'Processor')
plugin.register(
    'sparql', rdflib.query.Result,
    'rdfextras.sparql.query', 'SPARQLQueryResult')

tempFile = open('temp.rdf', 'r+')

#setup flickr api - http://stuvel.eu/media/flickrapi-docs/documentation/
api_key = 'dc2c74b6703a36da9316711ec76dca11'
api_secret = '9f904b83f4cf0f70'
flickr = flickrapi.FlickrAPI(api_key)

# stores photos from a given location into the triple store
# uses bounding boxes to get 
def storePhotosFrom(place):
    myBbox = ''
    if place == 'san francisco':
        myBbox = '-122.532,37.708,-122.368,37.813'
    elif place == 'los angeles':
        myBbox = '-122.532,37.708,-122.368,37.813'
    elif place == 'greece':
        myBbox = '-122.532,37.708,-122.368,37.813'
        
    photos = flickr.photos_search(has_geo='1', bbox=myBbox, per_page='10', accuracy='16')
    
    # store each photo in the triple store
    for photo in list(photos.iter('photo')):
        photoNode = BNode()
        g.add((photoNode, RDF.type, DC["Image"]))
        g.add((photoNode, DC["Identifier"], photo.attrib['id']))
        g.add((photoNode, DC["Title"], photo.attrib['title']))
        g.add((photoNode, DC["Creator"], photo.attrib['owner']))
        
    g.commit()
    
    # review temp rdf
    tempFile.write(str(len(g)))
    
    for s, p, o in g:
        tempFile.write('{} {} {}'.format(s,p,o))
        tempFile.write('\n')
        
        
# go through each photo in triple store and get geo details
def getPhotoInfo():
    photoIDs = g.query(
    """SELECT ?photoID
       WHERE {
          ?a dc:Identifier ?photoID .
       }""",
    initNs=dict(
        dc=DC))

    for row in photoIDs.result:
        # get photo details and store them
        photoDetails = flickr.photos_getInfo(photo_id=row)
        print(photoDetails.location.attrib['latitude'])
        print(row)
        
        
def storeUsers():
    # get all user ids of photos in triple store and retrieve/store details of them
    print("something")
        
def populateStore():
    # when I run both functions at the same time, it works, but when I turn the first function off, the triples do not appear. How do I keep the triples in the triple store?
    storePhotosFrom('san francisco')
    #getPhotoInfo()
    #storeUsers()
    
# main    
populateStore()

