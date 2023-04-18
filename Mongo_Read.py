import pymongo
import re

class TweetQuery:
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["twitter-covid2_updated"]
        self.collection = self.db["tweets"]

    def query_tweets_by_regex(self, regex_pattern):
        # Query tweets that match the regex pattern in the text field, ordered by popularity, and limit the results by 10
        tweets = self.collection.find({"text": {"$regex": regex_pattern, "$options": "i"}},{'text':1,'id_str':1, '_id':0}).sort("popularity", pymongo.DESCENDING).limit(10)
        return tweets

    def print_tweets_regex(self, tweets):
        for tweet in tweets:
            print(tweet)

#Constructor calling
#tweet_query = TweetQuery()

#Example Regex Pattern
#regex_pattern = input("Enter the regex pattern: ")
#limit = 10
#tweets = tweet_query.query_tweets_by_regex(regex_pattern)
#print(type(tweets))
#print(tweets)
#tweet_query.print_tweets_regex(tweets)

class TweetQuery_Hashtag:
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["twitter-covid2_updated"]
        self.collection = self.db["tweets"]

    def search_tweets_by_hashtags(self, hashtags):
        query = {"hashtags": {"$in": [hashtags]}}
        limit = 10
        tweets = self.collection.find(query,{'text':1,'_id':0}).sort("popularity", pymongo.DESCENDING).limit(limit)
        return tweets

    def print_tweets(self, tweets):
        for tweet in tweets:
            print(tweet)

#hashtag = TweetQuery_Hashtag()
#hashtags = input("Enter the hashtag pattern: ")
#limit = 10
#tweets = hashtag.search_tweets_by_hashtags(hashtags)
#print(type(tweets))
#hashtag.print_tweets(tweets)
#print(tweets)
#tweet_query.print_tweets_regex(tweets)