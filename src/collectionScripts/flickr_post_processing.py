# import rdflib
import flickrapi

from xml.etree import ElementTree
from pymongo import Connection, GEO2D
from xml.dom.minidom import parseString
from nltk import word_tokenize
import nltk
import progressbar
import yql
import sys

class FlickrPostProcessor():

    def __init__(self):

        #setup flickr api - http://stuvel.eu/media/flickrapi-docs/documentation/
        self.api_key = 'dc2c74b6703a36da9316711ec76dca11'
        self.api_secret = '9f904b83f4cf0f70'
        self.flickr = flickrapi.FlickrAPI(self.api_key)
        
        connection = Connection()
        db = connection['flickrDB']
        self.photoCollection = db.flickrCollection
        self.photoCollection.ensure_index( [("id", 1 )] )
        self.photoCollection.ensure_index( [("loc", GEO2D )] )
        self.photoCollection.ensure_index( [("place", 1 )] )
        
        
        API_KEY = 'dj0yJmk9UUY5TWxNMXBRb0M3JmQ9WVdrOVV6RlVOWFEzTjJzbWNHbzlNVGMzTVRBNE5EazJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD0zYQ--'
        SHARED_SECRET = '92a96753c369996f18b6a2ef4a6b1b9c85de04f5'
        self.y = yql.TwoLegged(API_KEY, SHARED_SECRET)
        self.yqlCache = {}
        
        
    
    # add details to each photo in mongo
    def findPhotoDetails(self):
        print 'findPhotoDetails started'
        
        count = self.photoCollection.count()
        counter = 0
        bar = progressbar.ProgressBar(maxval=count+1+500, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()
        
        # iterate through all photos in db
        photos = self.photoCollection.find()
        for photo in photos:
            if photo.get('server') is None:
                try:
                    photoDetails = self.flickr.photos_getInfo(photo_id=photo['id'])
                    photo['secret'] = photoDetails.find('photo').attrib['secret']
                    photo['server'] = photoDetails.find('photo').attrib['server']
                    photo['farm'] = photoDetails.find('photo').attrib['farm']
                    self.photoCollection.save(photo)
                except:
                    # perhaps a photo wasn't found
                    print "Exception Detected:", sys.exc_info()[0]
            counter = counter + 1
            bar.update(counter)
        
        bar.finish()        
        print 'Done finding photo details'
    
    def findUserLoc(self):
        print 'finding user locations'
        count = self.photoCollection.count()
        counter = 0
        bar = progressbar.ProgressBar(maxval=count+1, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()
        
        # iterate through all photos in db
        photos = self.photoCollection.find()
        for photo in photos:
            counter = counter + 1
            bar.update(counter)
            if photo.get('userLoc') is None and photo.get('ownerLocation') is not None:
                flickrUserLocation = photo['ownerLocation'].encode('utf-8')
                if self.yqlCache.get(flickrUserLocation) is not None and self.yqlCache[flickrUserLocation] != 0:
                    photo['userLoc'] = self.yqlCache[flickrUserLocation]
                    #print 'cacheSuccess: %20s %15s' % (flickrUserLocation, photo['id'])
                    self.photoCollection.save(photo) 
                elif flickrUserLocation == "":
                    print "Empty Location"
                else:
                    # send request out to YQL
                    yqlQuery = 'select * from geo.placefinder where text="%s";' % flickrUserLocation
                    #try:
                    yqlResult = self.y.execute(yqlQuery)
                    if yqlResult.rows == []:
                        # yql couldn't figure out where this is, so don't save a loc
                        self.yqlCache[flickrUserLocation] = 0
                        print 'fail: %20s %s' % (flickrUserLocation, photo['id'])
                    else:
                        # yql found a lat and lon, so let's tag it
                        loc = [float(yqlResult.rows[0].get('latitude')), float(yqlResult.rows[0].get('longitude'))]
                        photo['userLoc'] = loc
                        self.yqlCache[flickrUserLocation] = loc
                        #print 'success: %20s %15s %s' % (flickrUserLocation.decode('utf-8'), photo['id'], loc)
                        self.photoCollection.save(photo) 
                    #except:
                       # print "Exception Detected:", sys.exc_info()[0]
        bar.finish()        
        print 'Done finding user locations'                    
                   
                        
                
                
    
def main():
    print 'Beginning FlickrPostProcessor'
    x = FlickrPostProcessor()
    x.findPhotoDetails()
    #x.findUserLoc()
        
# main    

if __name__ == "__main__":
    main()    

