'''
Created on Mar 26, 2012

@author: cwerner
'''
from pymongo import Connection
from nltk.metrics import edit_distance
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk

class Linkage(object):
    def __init__(self):
        self.edit_dist_threshold = 0.2
        self.tweets = Connection().tweetsDB.tweetsCollection
        self.businesses = Connection().yelpDB.yelpBusinesses
        self.photos = Connection().flickrDB.flickrCollection
        self.linked = Connection().linkedDB.linkedCollection
        self.MAX_EDIT_DISTANCE = 100000000
        
    def unescape_html_chars(self, item):
        return item.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").replace("&quot;", "\"")
    
    def extract_tweet_ne(self, item):
        item = item.split()
        # Split the annotated text on whitespace, collect B/I items and join them together
        # Then return a list of named entities
        result = []
        cur_ne = []
        #print item
        for token in item:
            bio_tag = token.split("/")[-1]
            #print bio_tag
            # If we're starting/in the middle of an NE
            if bio_tag == "B-ENTITY" or bio_tag == "I-ENTITY":
                cur_ne.append(self.unescape_html_chars(token.split("/")[0]))
            # If we've hit an O and we have a previous NE, close it off 
            elif bio_tag == "O" and len(cur_ne) > 0:
                result.append(" ".join(cur_ne))
                cur_ne = []
        # If we've hit the end and ended with an NE
        if len(cur_ne) > 0:
            result.append(" ".join(cur_ne))
        return result
    
    def get_nearby_businesses(self, loc):
        return [_ for _ in self.businesses.find({"loc":{"$maxDistance":2, "$near":loc}}).limit(20)]
    
    def get_nearby_photos(self, loc):
        return [_ for _ in self.photos.find({"loc":{"$maxDistance":2, "$near":loc}}).limit(20)]
    
    def get_nearby_tweets(self, loc):
        return [_ for _ in self.tweets.find({"loc":{"$maxDistance":2, "$near":loc}}).limit(100)]
    
    def extract_normal_ne(self, text):
        result = []
        for sent in sent_tokenize(text) if text else []:
            for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
                if hasattr(chunk, "node"):
                    result.append(" ".join([c[0] for c in chunk.leaves()]))
        return result
    
    def yelp_twitter_linkage(self):
        # Record the number of matches just for information
        num_matches = 0
        for tweet in self.tweets.find():
            # One tweet had to be removed because it contained characters that
            # screwed up the NE and thus lacks the annotated field
            if "annotated" not in tweet:
                continue
            # Extract the named entities for comparison
            named_entities = self.extract_tweet_ne(tweet["annotated"].encode("UTF-8"))
            # Skip if we have no named entities in the tweet
            if not named_entities:
                continue
            #print "Tweet loc: %s" % tweet["loc"]
            #print "NE: %s" % named_entities
            # Examine the 20 closest businesses
            nearby_businesses = self.get_nearby_businesses(tweet["loc"])
            # Skip if there are no nearby businesses
            if not nearby_businesses:
                continue
            # For each NE in the tweet, compare to the 20 closest businesses
            for named_entity in named_entities:
                # Mark the smallest edit distance seen
                min_dist = self.MAX_EDIT_DISTANCE
                best_match = None
                for business in nearby_businesses:
                    # Get the edit distance between the Twitter NE and the business name
                    edit_dist = edit_distance(named_entity, business["name"])
                    # If it's the smallest seen so far, mark it
                    if edit_dist < min_dist:
                        min_dist = edit_dist
                        best_match = business
                # If it's below the threshold(originally 20% of the length of the best match)
                # then consider it a match
                if min_dist <= self.edit_dist_threshold * len(best_match["name"]):
                    #print "Good match for %s is: %s --> edit dist is: %d" % (named_entity, best_match, min_dist)
                    num_matches += 1
                    # Mark it in the linked db
                    self.linked.update({"id": "%s_%s" % (tweet["id"], best_match["id"])},
                                       {"tweetID":tweet["id"], "yelpID":best_match["id"]}, True)
        print "Yelp/Twitter: %d" % num_matches

    def yelp_flickr_linkage(self):
        num_matches = 0
        for item in self.photos.find():
            desc = item["description"].encode("UTF-8") if "description" in item and item["description"] else None
            title = item["title"].encode("UTF-8") if "title" in item and item["title"] else None
            if not desc and not title:
                continue
            named_entities = []
            named_entities.extend(self.extract_normal_ne(desc))
            named_entities.extend(self.extract_normal_ne(title))
            #print "DESC: %s" % desc
            #print "TITLE: %s" % title
            #print "NE: %s" % ne_list
            nearby_businesses = self.get_nearby_businesses(item["loc"])
            if not nearby_businesses:
                continue
            # Similar to the function above, iterate through the named entities in the photos
            # and compare to the Yelp business name. The best one, if within an edit distance
            # limit, is considered a match.
            for named_entity in named_entities:
                #print "NE ITEM: %s" % ne
                #print "NEARBY BUSINESSES: %s" % nearby_businesses
                min_dist = self.MAX_EDIT_DISTANCE
                best_match = None
                for business in nearby_businesses:
                    edit_dist = edit_distance(named_entity, business["name"])
                    if edit_dist < min_dist:
                        min_dist = edit_dist
                        best_match = business
                if min_dist <= self.edit_dist_threshold * len(best_match["name"]):
                    num_matches += 1
                    #print "Best match for %s is: %s" % (named_entity, best_match["name"])
                    self.linked.update({"id":"%s_%s" % (item["id"], best_match["id"])},
                                       {"flickrID":item["id"], "yelpID":best_match["id"]}, True)
        
        print "Yelp/Flickr matches: %d" % num_matches
        
    def flickr_twitter_linkage(self):
        num_matches = 0
            
        for tweet in self.tweets.find():
            if "annotated" not in tweet:
                continue
            
            named_entities = self.extract_tweet_ne(tweet["annotated"].encode("UTF-8"))
            if not named_entities:
                continue
            
            nearby_photos = self.get_nearby_photos(tweet["loc"])
            if not nearby_photos:
                continue
            
            for named_entity in named_entities:
                min_dist = self.MAX_EDIT_DISTANCE
                best_match = None
                
                for photo in nearby_photos:
                    photo_named_entities = []
                    desc = photo["description"].encode("UTF-8") if "description" in photo and photo["description"] else None
                    title = photo["title"].encode("UTF-8") if "title" in photo and photo["title"] else None
                    if not desc and not title:
                        continue
                    photo_named_entities.extend(self.extract_normal_ne(desc))
                    photo_named_entities.extend(self.extract_normal_ne(title))
                    
                    for photo_named_entity in photo_named_entities:
                        edit_dist = edit_distance(named_entity, photo_named_entity)
                        if edit_dist < min_dist:
                            min_dist = edit_dist
                            best_match = photo
                            
                if min_dist < self.MAX_EDIT_DISTANCE and min_dist <= self.edit_dist_threshold * len(best_match):
                    num_matches += 1
                    #print "MATCH for tweet NE %s: flickr %s" % (named_entity, best_match)
                    self.linked.update({"id":"%s_%s" % (tweet["id"], best_match["id"])},
                                           {"tweetID":tweet["id"], "flickrID":best_match["id"]}, True)
                        
        print "Flickr/tweet matches: %s" % num_matches
    
def main():
    l = Linkage()
    l.yelp_twitter_linkage()
    l.yelp_flickr_linkage()
    l.flickr_twitter_linkage()
if __name__=="__main__":
    main()