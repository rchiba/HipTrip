'''
Created on Mar 24 2012

@author: cwerner

This is simply for dumping the raw tweets(the text) so they can be annotated. The annotation occurs on Linux
only and they must be in newline formatted order so I strip newlines(replacing them with spaces) and
exported them to be annotated.
'''
from pymongo import Connection
def main():
    conn = Connection()
    tweets = conn.tweetsDB.tweetsCollection
    tweets_cursor = tweets.find()
    
    parsed_tweets = []
    for tweet in tweets_cursor:
        #if tweet["id"] == "178728337844338688":
        #    continue
        #tweet_text = (tweet["id"] + " " + tweet["text"]).encode("UTF-8").replace("\n", " ")
        tweet_text = tweet["text"].encode("UTF-8").replace("\n", " ")
        parsed_tweets.append(tweet_text)
    out_file = open("tweets_parsed.txt", "w")
    out_file.write("\n".join(parsed_tweets))
    out_file.close()
    
if __name__ == "__main__":
    main()