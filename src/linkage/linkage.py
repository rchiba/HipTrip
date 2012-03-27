'''
Created on Mar 26, 2012

@author: cwerner
'''
from pymongo import Connection
from nltk.metrics import edit_distance
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
    
    def extract_ne(self, item):
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
        
    def yelp_twitter_linkage(self):
        # Record the number of matches just for information
        num_matches = 0
        for tweet in self.tweets.find():
            # One tweet had to be removed because it contained characters that
            # screwed up the NE and thus lacks the annotated field
            if "annotated" not in tweet:
                continue
            # Extract the named entities for comparison
            named_entities = self.extract_ne(tweet["annotated"].encode("UTF-8"))
            # Skip if we have no named entities in the tweet
            if not named_entities:
                continue
            #print "Tweet loc: %s" % tweet["loc"]
            #print "NE: %s" % named_entities
            # Examine the 20 closest businesses
            nearby_businesses = [_ for _ in self.businesses.find({"loc":{"$near":tweet["loc"]}}).limit(20)]
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
                        best_match = business["name"]
                # If it's below the threshold(originally 20% of the length of the best match)
                # then consider it a match
                if min_dist <= self.edit_dist_threshold * len(best_match):
                    #print "Good match for %s is: %s --> edit dist is: %d" % (named_entity, best_match, min_dist)
                    num_matches += 1
                    # Mark it in the linked db
                    self.linked.update({"id": "%s_%s" % (tweet["id"], business["id"])},
                                       {"tweetID":tweet["id"], "yelpID":business["id"]}, True)
        print "NUM MATCHES: %d" % num_matches

    def yelp_flickr_linkage(self):
        return
    
    def flickr_twitter_linkage(self):
        return
    
def main():
    Linkage().yelp_twitter_linkage()
    
if __name__=="__main__":
    main()