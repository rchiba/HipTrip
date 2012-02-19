import tweepy

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="QwuBMbP2f9FQYoZBjF8fSA"
consumer_secret="Dvc4NEfSoYXdORxVRMdLkXkHMGO8PSxkkqL479XrFL4"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="8950292-DjfCvEpXTKbmb0TVZIP7XwAga2ua21LrFxglt0"
access_token_secret="DZX2rSmd6NpGUHXIJczq0OGYisBCFnQg6Dh6qu4oM"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print "Twitter collection script running under "+api.me().name


def storeTweetsFor(location):
    