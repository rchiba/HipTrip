from instagram.client import InstagramAPI

access_token = "..."
api = InstagramAPI(client_id="440b5489023747b2bb6c1a65ddb7f557", client_secret="ea56eb3f42894bfcb3dbe1eb2ab338da", redirect_uri="http://www.hiptrip.us")
popular_media = api.media_popular(count=20)
for media in popular_media:
    print media.images['standard_resolution']