'''
Created on Mar 29, 2012

@author: rchiba
@description: run this script after pulling in yelp entries 
this script
- generates indexed tags to make string searches fast


'''
from pymongo import Connection
from nltk import word_tokenize
import nltk
import progressbar

class YelpPostProcessor():
    def __init__(self):
        self.yelp_db = Connection()["yelpDB"]
        self.yelp_collection = self.yelp_db["yelpCollection"]
        
        
    # generating some tags to index by so we can do string search
    def generateKeywords(self):
        yelpEntries = self.yelp_collection.find()
        count = self.yelp_collection.count()
        bar = progressbar.ProgressBar(maxval=count+1, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()
        counter = 0    
        for entry in yelpEntries:
            if entry.get("name") is not None:
                keywords = "%s %s" % ("", entry["name"].encode('ascii', 'ignore'))
            if entry.get("snippet_text") is not None:
                keywords = "%s %s" % (keywords, entry["snippet_text"].encode('ascii', 'ignore'))
            keywords = keywords.lower() # case insensitive
            keywords = word_tokenize(keywords) # word tokens without stopwords
            keywords = [w for w in keywords if not w in nltk.corpus.stopwords.words('english')]
            keywords = [w for w in keywords if len(w) > 2] #words longer than 2 letters
            entry["_keywords"] = keywords
            #print keywords
            self.yelp_collection.save(entry)
            counter = counter + 1
            bar.update(counter)
            
        bar.finish()
        print "- generated keywords"
            
def main():
    print "Beginning Yelp Postprocess (this may take a minute)"
    x = YelpPostProcessor()
    x.generateKeywords()
    
    print "Finished Yelp Postprocess"
if __name__ == "__main__":
    main()