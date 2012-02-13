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

from xml.dom.minidom import parseString

#setup store
# http://code.google.com/p/rdflib/w/list
# http://readthedocs.org/docs/rdflib/en/latest/persistence.html
default_graph_uri = "http://localhost/rdfstore"
store = plugin.get('Sleepycat', Store)('rdfstore')
#Open previously created store, or create it if it doesn't exist yet
g = Graph(store="Sleepycat",
               identifier = URIRef(default_graph_uri))
path = 'rdfstore' #mkdtemp()
rt = g.open(path, create=False)
if rt == NO_STORE:
#    There is no underlying Sleepycat infrastructure, create it
    print('No store detected - creating store')
    g.open(path, create=True)
else:
    print('Existing store detected')
    assert rt == VALID_STORE, "The underlying store is corrupt"

#setup graph
# g=rdflib.Graph(store='Sleepycat')
# g.open("rdfstore")



g.bind("dc", "http://purl.org/dc/elements/1.1/")
dcURL = "http://purl.org/dc/elements/1.1/"
DC = Namespace(dcURL)

geo = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
g.bind("geo", "http://www.w3.org/2003/01/geo/wgs84_pos#")

foaf = Namespace('http://xmlns.com/foaf/0.1/')
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

tempFile = open('temp.rdf', 'r+')

#setup flickr api - http://stuvel.eu/media/flickrapi-docs/documentation/
api_key = 'dc2c74b6703a36da9316711ec76dca11'
api_secret = '9f904b83f4cf0f70'
flickr = flickrapi.FlickrAPI(api_key)
# stores photos from a given location into the triple store
# uses bounding boxes to get 
# I wonder how many queries before I get limited? hmmm
def storePhotosFrom(place):
    myBbox = ''
    minTakenDate='1328081477' # date from which photos are searched
    page = 0
    pages = 1
    if place == 'san francisco':
        myBbox = '-122.532,37.708,-122.368,37.813'
    elif place == 'los angeles':
        myBbox = '-122.532,37.708,-122.368,37.813'
    elif place == 'greece':
        myBbox = '-122.532,37.708,-122.368,37.813'
        
    while page < pages:
        page += 1
        photos = flickr.photos_search(has_geo='1', bbox=myBbox, page=page, per_page='200', accuracy='16', min_taken_date=minTakenDate)
        #print(ElementTree.tostring(photos))
        pages = int(photos.find('photos').attrib["pages"])
        page = int(photos.find('photos').attrib["page"])
        print(str(page)+" out of "+str(pages))
        # store each photo in the triple store
        for photo in list(photos.iter('photo')):
            g.add((custom[photo.attrib['id']], RDF.type, DC["Image"]))
            g.add((custom[photo.attrib['id']], DC["Identifier"], photo.attrib['id']))
            g.add((custom[photo.attrib['id']], DC["Title"], photo.attrib['title']))
            g.add((custom[photo.attrib['id']], DC["Creator"], custom[photo.attrib['owner']]))
        
    g.commit()
        
# go through each photo in triple store and get geo details
def getPhotoInfo():
    print "getPhotoInfo()"
    photoIDs = g.query(
    """SELECT ?photoID
       WHERE {
          ?a dc:Identifier ?photoID .
       }""",
    initNs=dict(
        dc=DC))

    for idx, row in enumerate(photoIDs.result):
        # get photo details and store them
        #print(row)
        print(str(idx)+" out of "+str(len(photoIDs.result)))
        photoID = row
        photoDetails = flickr.photos_getInfo(photo_id=row)
        #print(ElementTree.tostring(photoDetails))
        latitude = photoDetails.find('photo').find('location').attrib['latitude']
        longitude = photoDetails.find('photo').find('location').attrib['longitude']
        posted = photoDetails.find('photo').find('dates').attrib['posted']
        ownerId = photoDetails.find('photo').find('owner').attrib['nsid']
        ownerLocation = photoDetails.find('photo').find('owner').attrib['location']
        realname = photoDetails.find('photo').find('owner').attrib['realname']
        username = photoDetails.find('photo').find('owner').attrib['username']
        
        # assert in triple store
        g.add((custom[photoID], geo['lat'], latitude))
        g.add((custom[photoID], geo['lon'], longitude))
        g.add((custom[photoID], DC['dateSubmitted'], posted))
        g.add((custom[ownerId], RDF.type, foaf['Person']))
        g.add((custom[ownerId], foaf['based_near'], ownerLocation))
        g.add((custom[ownerId], foaf['name'], realname))
        g.add((custom[ownerId], custom['username'], username))
        
def storeUsers():
    # get all user ids of photos in triple store and retrieve/store details of them
    print("something")
        
def populateStore():
    # when I run both functions at the same time, it works, but when I turn the first function off, the triples do not appear. How do I keep the triples in the triple store?
    #storePhotosFrom('san francisco')
    getPhotoInfo()
    #storeUsers()
    
    # review temp rdf
    tempFile.write(str(len(g)))
    
    for s, p, o in g:
        tempFile.write((s+" "+p+" "+o).encode('utf-8'))
        tempFile.write('\n')
    
    g.close()
    
# main    
populateStore()

