import pymongo
import re

class TweetQuery:
    def __init__(self, db_name, collection_name):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def query_tweets_by_regex(self, regex_pattern, limit=10):
        # Query tweets that match the regex pattern in the text field, ordered by popularity, and limit the results by 10
        tweets = self.collection.find({"text": {"$regex": regex_pattern, "$options": "i"}}).sort("popularity", pymongo.DESCENDING).limit(limit)
        return tweets

    def print_tweets_regex(self, tweets):
        for tweet in tweets:
            self.print_tweet_info(tweet)

#Constructor calling
tweet_query = TweetQuery("twitter-covid2_updated", "tweets")

#Example Regex Pattern
regex_pattern = input("Enter the regex pattern: ")
limit = 10
tweets = tweet_query.query_tweets_by_regex(regex_pattern, limit)

class TweetQuery_Hashtag:
    def __init__(self, db_name, collection_name):
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def search_tweets_by_hashtags(self, hashtags):
        query = {"hashtags": {"$in": hashtags}}
        sort_by = [("popularity", pymongo.DESCENDING)]
        limit = 10
        tweets = self.collection.find(query).sort(sort_by).limit(limit)
        return tweets

    def print_tweet_info(self, tweet):
        print(tweet)

    def print_tweets(self, tweets):
        for tweet in tweets:
            self.print_tweet_info(tweet)