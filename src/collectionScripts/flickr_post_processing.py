# import rdflib
import flickrapi

from xml.etree import ElementTree
from pymongo import Connection, GEO2D
from xml.dom.minidom import parseString
from nltk import word_tokenize
import nltk
import progressbar

class FlickrPostProcessor():

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
            self.myBbox = '-118.55,33.84,-118.16,34.15'
        elif place == 'greece':
            self.myBbox = ' '
        
        self.place = place
        
        connection = Connection()
        db = connection['flickrDB']
        self.photoCollection = db.flickrCollection
        self.photoCollection.ensure_index( [("id", 1 )] )
        self.photoCollection.ensure_index( [("loc", GEO2D )] )
        self.photoCollection.ensure_index( [("place", 1 )] )
    
    # add details to each photo in mongo
    def findPhotoDetails(self):
        print 'findPhotoDetails started'
        
        page = 0
        pages = 1
        
        count = self.photoCollection.count()
        bar = progressbar.ProgressBar(maxval=count+1, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()
            
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
                ownerLocation = photoDetails.find('photo').find('owner').attrib['location'].encode('utf-8')
                realname = photoDetails.find('photo').find('owner').attrib['realname']
                username = photoDetails.find('photo').find('owner').attrib['username']
                
                
                #print photo.attrib['id']
                key = {"id": id}
                photoObj = {
                    "id": id,
                    "title": title,
                    "description":description,
                    "loc": [float(latitude), float(longitude)],
                    "createdAt": posted,
                    "ownerID": ownerId,
                    "ownerLocation": ownerLocation,
                    "ownerName": realname,
                    "ownerUsername": username,
                    "place": self.place
                }
                # this should take care of duplicate insertions
                self.photoCollection.update(key, photoObj, True);
                
        print 'Done finding photo details'
    
    
def main():
    print 'Beginning FlickrPostProcessor'
    x = FlickrPostProcessor()
    x.findPhotoDetails()

        
# main    

if __name__ == "__main__":
    main()    

