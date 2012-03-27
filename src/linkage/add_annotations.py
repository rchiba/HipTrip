'''
Created on Mar 25, 2012

@author: cwerner

Script to update each tweet object with an NER tagged annotation of the text(for linkage).
It requires the newline separated corpus in combined.txt. 
'''
from pymongo import Connection

def main():
    annotated_tweets = open("combined.txt", "r").readlines()
    conn = Connection()
    tweets_coll = conn["tweetsDB"]["tweetsCollection"]
    i = 0
    while i < len(annotated_tweets):
        tweet = annotated_tweets[i]
        annotated = annotated_tweets[i+1]
        tweet_id = tweet.split()[0]

        #print tweet, annotated.rstrip()
        tweet_db = tweets_coll.find({"id":tweet_id})
        if tweet_db.count() == 1:
            #print tweet, annotated.rstrip()
            #print "Tweet in db: %s" % tweet_db[0]
            tweets_coll.update({"id":tweet_id},{"$set":{"annotated":annotated.rstrip()}})
            #print tweets_coll.update({"id":tweet_id}, tweet_db[0])
        else:
            print "Not found"
        i += 2
        
if __name__ == "__main__":
    main()