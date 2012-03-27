'''
Created on Feb 20, 2012

@author: cwerner
'''
import oauth2
import urllib2
import json
from pymongo import Connection
YELP_CONSUMER_KEY = "6kXOKeAmTEeGYA0XPJc4ZQ"
YELP_CONSUMER_SECRET = "LA42ssT3tBA6oYcekLpmLUeNDQA"
YELP_TOKEN = "vflPeUWVbykujnEWRkygh_fU37tathXG"
YELP_TOKEN_SECRET = "8qoApZxxfNsKzcWhU48mxyfjxQY"

KEYS = [{"CONSUMER_KEY":"cYKG9_XPg_xu5amBZxvBpw",
         "CONSUMER_SECRET":"z-5VV_RkeV_UAA99wi0-Uu9jggk",
         "TOKEN":"YM7HAInf0UI51e3Q95_E7ykFneZ6Notc",
         "TOKEN_SECRET":"RECW_KtBs0KNSoGRn81hiRB6rY4"
         },
        {"CONSUMER_KEY":"6kXOKeAmTEeGYA0XPJc4ZQ",
         "CONSUMER_SECRET":"LA42ssT3tBA6oYcekLpmLUeNDQA",
         "TOKEN":"vflPeUWVbykujnEWRkygh_fU37tathXG",
         "TOKEN_SECRET":"8qoApZxxfNsKzcWhU48mxyfjxQY"
         },
        {"CONSUMER_KEY":"9GmWmLbrYUysUmzuJUTlSQ",
         "CONSUMER_SECRET":"Dx3y7SWEDLAX1H0Se1IG7xTWTGg",
         "TOKEN":"IsH6JdhJx0j-e2K3oEqBT_1IZtSmc5QZ",
         "TOKEN_SECRET":"Dnss35dm_FTvm0V7kvl_CggQkzM"
         },
        {"CONSUMER_KEY":"hJFAS93qFFjFdEP3-qSkiw",
         "CONSUMER_SECRET":"yom-g4M8nbvtOF5pdi0ofbUdVyU",
         "TOKEN":"SzN10y5MxriverhymGnIIttAsrivgLk9",
         "TOKEN_SECRET":"fql4fEmZUHPNN_PteG0egBAYKpo"
         },
        {"CONSUMER_KEY":"WJOHCBNwyP4WZ7-K-8nebg",
         "CONSUMER_SECRET":"V2U4oMMi9ElPKBW5INKpoItQrho",
         "TOKEN":"qfnSqn9Y2pyEuSHPV-Np3qy0r6Nz8q6Y",
         "TOKEN_SECRET":"wIUbwhcATtH7IdX6TQiCC2Ys-mc"
         },
        {"CONSUMER_KEY":"qrNPHYsLSu1DQ-i55yEEWQ",
         "CONSUMER_SECRET":"1JmrGIV49eu8o-Wv_TTFoEinXHw",
         "TOKEN":"nBJ8pffoVYcCaEJG13sUFf15G1kFObzu",
         "TOKEN_SECRET":"Jevf-IfM0R41BM6rQKM79Kxu3P8"
         },
        {"CONSUMER_KEY":"r6IhcvA_Y4xBDUsJMZ1bLw",
         "CONSUMER_SECRET":"3lT3-wYp-JvZnZ6prPjkRKu84pQ",
         "TOKEN":"KQ7mJTNocagdqOyP1M6wCKWlPnL4oeYL",
         "TOKEN_SECRET":"M4ZT5m44YtVnVUtGJ-LC5bRhuEM"
         }
        ]

class YelpDataScraper():
    def __init__(self):
        self.yelp_url = "http://api.yelp.com/v2/search?sort=2&term=%s&location=San+Francisco&cll=%s&limit=20"
        self.yelp_db = Connection()["yelpDB"]
        self.yelp_collection = self.yelp_db["yelpBusinesses"]
        self.business_offset = 0
        self.current_index = 0
        
    def request(self, url):
        consumer = oauth2.Consumer(KEYS[self.current_index]["CONSUMER_KEY"], KEYS[self.current_index]["CONSUMER_SECRET"])
        oauth_request = oauth2.Request("GET", url, {})
        oauth_request.update({"oauth_nonce":oauth2.generate_nonce(),
                              "oauth_timestamp":oauth2.generate_timestamp(),
                              "oauth_token":KEYS[self.current_index]["TOKEN"],
                              "oauth_consumer_key":KEYS[self.current_index]["CONSUMER_KEY"]
                              })
        token = oauth2.Token(KEYS[self.current_index]["TOKEN"], KEYS[self.current_index]["TOKEN_SECRET"])
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        signed_url = oauth_request.to_url()
        
        try:
            page = urllib2.urlopen(signed_url)
            response = json.loads(page.read())
        except urllib2.HTTPError, error:
            print json.loads(error.read())
            self.current_index += 1
            return self.request(url)
        return response
    
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
    
    def unescape_html_chars(self, item):
        return item.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").replace("&quot;", "\"")
    
    def populate_store(self):
        for tweet in Connection()["tweetsDB"]["tweetsCollection"].find():
            named_entities = self.extract_ne(tweet["annotated"].encode("UTF-8")) if "annotated" in tweet else []
            # Query Yelp for the tweet
            for ne in named_entities:
                #print ne
                try:
                    ne = urllib2.quote(ne)
                except:
                    continue
                response = self.request(self.yelp_url % (urllib2.quote(ne), map(str, tweet["loc"])))

                if not response:
                    print "LIMIT HIT!"
                    return
                
                if "businesses" not in response:
                    print "ERROR! Business data should contain businesses key."
                    return
                
                for business in response["businesses"]:
                    if "location" not in business or "coordinate" not in business["location"]:
                        location = None
                    else:
                        location = [business["location"]["coordinate"]["latitude"], business["location"]["coordinate"]["longitude"]]
                    key = {"id":business["id"]}
                    yelp_business = {"id":business["id"],
                                     "name":business["name"],
                                     "loc":location,
                                     "rating":business["rating"] if "rating" in business else None,
                                     "snippet_text":business["snippet_text"] if "snippet_text" in business else None,
                                     "display_address":business["display_address"] if "display_address" in business else None,
                                     "address":business["address"] if "address" in business else None,
                                     "url":business["url"] if "url" in business else None,
                                     "image_url":business["image_url"] if "image_url" in business else None
                                     }
                    #print "YELP BUSINESS: %s" % yelp_business
                    self.yelp_collection.update(key, yelp_business, True)
#        while True:
#            response = self.request(self.yelp_url % self.business_offset)
#            if not response:
#                print "Limit hit"
#                return
#
#            if "businesses" not in response:
#                print "ERROR! Response data should contain businesses key."
#                return
#            print "# businesses: %d" % len(response["businesses"])
#            print "Offset: %d" % self.business_offset
#            print response["businesses"]
#            for business in response["businesses"]:
#                if "location" not in business or "coordinate" not in business["location"]:
#                    print "Missing location"
#                    continue
#                key = {"id":business["id"]}
#                yelp_business = {"id":business["id"],
#                                 "name":business["name"],
#                                 "loc":[business["location"]["coordinate"]["latitude"], business["location"]["coordinate"]["longitude"]],
#                                 "rating":business["rating"] if "rating" in business else None,
#                                 "snippet_text":business["snippet_text"] if "snippet_text" in business else None,
#                                 "display_address":business["display_address"] if "display_address" in business else None,
#                                 "address":business["address"] if "address" in business else None,
#                                 "url":business["url"] if "url" in business else None,
#                                 "image_url":business["image_url"] if "image_url" in business else None
#                                 }
#                self.yelp_collection.update(key, yelp_business, True)
#                #print business
#            
#            self.business_offset += 20
#            if len(response["businesses"]) < 20:
#                break
            
def main():
    x = YelpDataScraper()
    x.populate_store()
    
if __name__ == "__main__":
    main()