from instagram.client import InstagramAPI

access_token = "..."
api = InstagramAPI(client_id="440b5489023747b2bb6c1a65ddb7f557", client_secret="ea56eb3f42894bfcb3dbe1eb2ab338da", redirect_uri="http://www.hiptrip.us")
popular_media = api.media_popular(count=20)
for media in popular_media:
    print media.images['standard_resolution']
    
    
class InstagramDataScraper():
    def __init__(self):
        print 'init'
        
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