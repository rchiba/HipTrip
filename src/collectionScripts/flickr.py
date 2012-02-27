# import rdflib
import flickrapi

from xml.etree import ElementTree

# from rdflib.graph import Graph
# from rdflib import Literal, BNode, Namespace
# from rdflib import RDF
# from rdflib.graph import ConjunctiveGraph as Graph
# from rdflib import plugin
# from rdflib.store import Store, NO_STORE, VALID_STORE
# from rdflib.namespace import Namespace
# from rdflib.term import Literal
# from rdflib.term import URIRef
# from tempfile import mkdtemp
from pymongo import Connection
from xml.dom.minidom import parseString

class FlickrDataScraper():

    def __init__(self, place):

        #setup flickr api - http://stuvel.eu/media/flickrapi-docs/documentation/
        self.api_key = 'dc2c74b6703a36da9316711ec76dca11'
        self.api_secret = '9f904b83f4cf0f70'
        self.flickr = flickrapi.FlickrAPI(self.api_key)
        
        #query params
        self.minTakenDate = '1328081477' # date from which photos are searched
        self.per_page='200' # 200 is max
        self.accuracy='14' # minimum accuracy to be returned (16 is POI level granularity)
        
        if place == 'san francisco':
            self.myBbox = '-122.532,37.708,-122.368,37.813'
        elif place == 'los angeles':
            self.myBbox = ' '
        elif place == 'greece':
            self.myBbox = ' '
        
        connection = Connection()
        db = connection['flickrDB']
        self.photoCollection = db.flickrCollection
    
    # stores photos from a given location into the triple store
    # uses bounding boxes to get 
    # I wonder how many queries before I get limited? hmmm
    def storePhotos(self):
        print 'Starting queries'
        
        page = 0
        pages = 1
            
        while page < pages:
            page += 1
            photos = self.flickr.photos_search(has_geo='1', bbox=self.myBbox, page=page, per_page=self.per_page, accuracy=self.accuracy, min_taken_date=self.minTakenDate)
            #print(ElementTree.tostring(photos))
            pages = int(photos.find('photos').attrib["pages"]) #set to this so you can get all the pages
            page = int(photos.find('photos').attrib["page"]) + 1 
            print "%s out of %s pages" % (page, pages)
            # store each photo in the triple store
            
            # for each photo returned from the photos.search API
            for photo in list(photos.iter('photo')):
                # make a call to the photos.details API to get more fields 
                photoDetails = self.flickr.photos_getInfo(photo_id=photo.attrib['id'])
                id=photo.attrib['id']
                title=photo.attrib['title'].encode('utf-8')
                latitude = photoDetails.find('photo').find('location').attrib['latitude']
                longitude = photoDetails.find('photo').find('location').attrib['longitude']
                description = photoDetails.find('photo').find('description').text #this might break
                posted = photoDetails.find('photo').find('dates').attrib['posted']
                ownerId = photoDetails.find('photo').find('owner').attrib['nsid']
                ownerLocation = photoDetails.find('photo').find('owner').attrib['location']
                realname = photoDetails.find('photo').find('owner').attrib['realname']
                username = photoDetails.find('photo').find('owner').attrib['username']
                
                
                #print photo.attrib['id']
                key = {"id": id}
                photoObj = {
                    "id": id,
                    "title": title,
                    "description":description,
                    "lat": latitude,
                    "lon": longitude,
                    "createdAt": posted,
                    "ownerID": ownerId,
                    "ownerLocation": ownerLocation,
                    "ownerName": realname,
                    "ownerUsername": username,
                }
                # this should take care of duplicate insertions
                self.photoCollection.update(key, photoObj, True);
                print "%s: taken at %s in %9s %9s %s" % (id, posted, latitude, longitude, ownerLocation)
                
        print 'Done storing photos'
            
    def storeUsers():
        # get all user ids of photos in triple store and retrieve/store details of them
        print("something... might not need this function if we just use ownerLocation")
            
    
    
def main():
    print 'Beginning FlickrDataScraper'
    # when I run both functions at the same time, it works, but when I turn the first function off, the triples do not appear. How do I keep the triples in the triple store?
    #storePhotosFrom('san francisco')
    x = FlickrDataScraper('san francisco')
    x.storePhotos()
    #storeUsers()
    
    # review temp rdf
    # tempFile.write(str(len(g)))
    
    # for s, p, o in g:
        # tempFile.write((s+" "+p+" "+o).encode('utf-8'))
        # tempFile.write('\n')
    
    # g.close()
        
# main    

if __name__ == "__main__":
    main()    

