'''
Created on Feb 20, 2012

@author: cwerner
'''
from rdflib import Namespace, plugin
from rdflib.graph import Graph
from rdflib.query import Processor, Result
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib.term import Literal, URIRef
from json import loads
import oauth2
import urllib2

YELP_CONSUMER_KEY = "6kXOKeAmTEeGYA0XPJc4ZQ"
YELP_CONSUMER_SECRET = "LA42ssT3tBA6oYcekLpmLUeNDQA"
YELP_TOKEN = "vflPeUWVbykujnEWRkygh_fU37tathXG"
YELP_TOKEN_SECRET = "8qoApZxxfNsKzcWhU48mxyfjxQY"

class YelpDataScraper():
    def __init__(self):
        default_graph_uri = "http://example.com/rdfstore"
        config_string = "rdfstore"
        # Register plugins
        plugin.register("sparql", Processor, "rdfextras.sparql.processor", "Processor")
        plugin.register("sparql", Result, "rdfextras.sparql.query", "SPARQLQueryResult")
        
        store = plugin.get("Sleepycat", Store)("rdfstore")
        rt = store.open(config_string, create=False)
        if rt == NO_STORE:
            store.open(config_string, create=True)
        else:
            assert rt == VALID_STORE, "The underlying store is corrupted" 
        
        self.graph = Graph(store, identifier=URIRef(default_graph_uri))
        self.graph.bind("dc", "http://purl.org/dc/elements/1.1/")
        self.graph.bind("geo", "http://www.w3.org/2003/01/geo/wgs84_pos#")
        self.graph.bind("foaf", "http://xmlns.com/foaf/0.1/")
        self.graph.bind("custom", "http://localhost")
        
        self.namespaces = {"dc":Namespace("http://purl.org/dc/elements/1.1/"),
                           "geo":Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#"),
                           "foaf":Namespace("http://xmlns.com/foaf/0.1/"),
                           "custom":Namespace("http://localhost/")}
        
        self.yelp_url = "http://api.yelp.com/v2/search?search=2&location=San+Francisco"
        
    def request(self, url):
        consumer = oauth2.Consumer(YELP_CONSUMER_KEY, YELP_CONSUMER_SECRET)
        oauth_request = oauth2.Request("GET", url, {})
        oauth_request.update({"oauth_nonce":oauth2.generate_nonce(),
                              "oauth_timestamp":oauth2.generate_timestamp(),
                              "oauth_token":YELP_TOKEN,
                              "oauth_consumer_key":YELP_CONSUMER_KEY
                              })
        token = oauth2.Token(YELP_TOKEN, YELP_TOKEN_SECRET)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        signed_url = oauth_request.to_url()
        
        try:
            page = urllib2.urlopen(signed_url)
            response = loads(page.read())
        except urllib2.HTTPError, error:
            print loads(error.read())
            return None
        return response
    
    def populate_store(self):
        response = self.request(self.yelp_url)
        yelp_url = "http://www.yelp.com/%s"
        if "businesses" not in response:
            print "ERROR! Response data should contain businesses key."
            return
        
        for business in response["businesses"]:
            self.graph.add((URIRef(yelp_url % business["id"]), self.namespaces["foaf"]["name"], Literal(business["name"])))
            self.graph.add((URIRef(yelp_url % business["id"]), self.namespaces["dc"]["Image"], URIRef(business["image_url"])))
            self.graph.add((URIRef(yelp_url % business["id"]), self.namespaces["geo"]["lat"], business["location"]["coordinate"]["latitude"]))
            self.graph.add((URIRef(yelp_url % business["id"]), self.namespaces["geo"]["lon"], business["location"]["coordinate"]["longitude"]))
            self.graph.add((URIRef(yelp_url % business["id"]), self.namespaces["dc"]["rating"], business["rating"]))
            #print business
    
    def query_store(self):
        # To iterate over all triples:
#        for (s,p,o) in self.graph.triples((None, None, None)):
#            print (s,p,o)
#        return

        # Query for a specific subject
        qres = self.graph.query("""
            SELECT DISTINCT ?p ?o
            WHERE {
                <http://www.yelp.com/cc-rider-motorcycle-tow-san-francisco-2> ?p ?o
            }""", initNs=self.namespaces)
        
        for row in qres.result:
            print row
            
def main():
    x = YelpDataScraper()
    x.populate_store()
    print "Tuples in graph: %s" % len(x.graph)
    x.query_store()
    
if __name__ == "__main__":
    main()