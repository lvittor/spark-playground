import tweepy
from tweepy import StreamRule
import os

# Twitter API credentials
bearer_token = os.environ.get("BEARER_TOKEN")

class TweetChild:
    def __init__(self, text, created_at, author_id, geo, lang):
        self.text = text
        self.created_at = created_at
        self.author_id = author_id
        self.geo = geo
        self.lang = lang
    
    def __str__(self) -> str:
        return f"TweetChild(text={self.text}, created_at={self.created_at}, author_id={self.author_id}, geo={self.geo}, lang={self.lang})"

class TwitterStreamHandler(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        tweet_child = TweetChild(tweet.text, tweet.created_at, tweet.author_id, tweet.geo, tweet.lang)
        print(tweet_child)
        print("")


stream = TwitterStreamHandler(bearer_token)
# printer.add_rules([StreamRule("is:verified", tag="verified")])
stream.filter(tweet_fields="created_at,author_id,geo,lang")
# printer.sample()