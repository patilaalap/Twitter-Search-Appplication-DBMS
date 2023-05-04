# Code Done by Abhishek

import pymongo
import time

class TweetQuery:
    def __init__(self):
        # Establish a connection
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["twitter-covid3"]
        self.coll_tweets = self.db["tweets"]
        self.coll_comments = self.db["comments"]

    # Query to get tweets for a text search
    def query_tweets_by_regex(self, regex_pattern, offset):
        tweets = self.coll_tweets.find({"text": {"$regex": regex_pattern, "$options": "i"}}, {'_id':0}).sort(
            "popularity", pymongo.DESCENDING).skip(offset).limit(10)
        return self.get_details_list(tweets)


    # Query to get tweets by hashtag search
    def search_tweets_by_hashtags(self, hashtags, offset):
        query = {"hashtags": {"$in": [hashtags]}}
        limit = 10
        tweets = self.coll_tweets.find(query, {'_id':0}).sort(
            "popularity", pymongo.DESCENDING).skip(offset).limit(limit)
        return self.get_details_list(tweets)


    # Query to get detailed tweet info
    def get_tweet_details(self, tweet_id):
        tweet = self.coll_tweets.find({"id_str": tweet_id}, {'_id':0})
        return self.get_details_list(tweet)

    # Query to get comments on a tweet
    def get_comments_for_tweet(self, tweet_id):
        comments = self.coll_comments.find({"in_reply_to_status_id_str": tweet_id},{'id':0}).hint(
            'in_reply_to_status_id_str_1').sort("created_at", pymongo.DESCENDING)
        return self.get_details_list(comments)

    # Query to get a users tweets
    def get_tweets_by_username(self, username):
        tweets = self.coll_tweets.find({"user_name": username},{'_id':0}).hint('user_name_1').sort("timestamp", pymongo.DESCENDING)
        return self.get_details_list(tweets)


    # Query to get the top10 tweets
    def get_top_10_popular_tweets(self):
        top_tweets = self.coll_tweets.find().sort("popularity", pymongo.DESCENDING).limit(10)
        return self.get_details_list(top_tweets)


    # Function to return the result as a list
    def get_details_list(self, result):
        L= []
        for detail in result:
            L.append(detail)
        return L


    # Query to get sentiment of a tweet
    def get_sentiment(self,tweet_id):
        sentiment = self.coll_tweets.find({"id_str": tweet_id},{"sentiment":1,"_id":0})
        return self.get_details_list(sentiment)


    # Query to get top10 tweets of the day
    def top10_by_day(self):
        #curr_time = time.time()
        curr_time = 1587826117
        top_tweets = self.coll_tweets.find({'timestamp': {'$gte': (curr_time - 60*60*24)}}).sort\
            ("popularity", pymongo.DESCENDING).limit(10)
        return self.get_details_list(top_tweets)


    # Query to get top10 tweets of the week
    def top10_by_week(self):
        # curr_time = time.time()
        curr_time = 1587826117
        top_tweets = self.coll_tweets.find({'timestamp': {'$gte': (curr_time - 60 * 60 * 24*7)}}).sort\
            ("popularity",pymongo.DESCENDING).limit(10)
        return self.get_details_list(top_tweets)


    # Query to get top10 tweets of the month
    def top10_by_month(self):
        # curr_time = time.time()
        curr_time = 1587826117
        top_tweets = self.coll_tweets.find({'timestamp': {'$gte': (curr_time - 60 * 60 * 24 * 30)}}).sort\
            ("popularity",pymongo.DESCENDING).limit(10)
        return self.get_details_list(top_tweets)


    # Query to get tweets by hashtag of last day
    def hash_by_day(self, hashtags):
        # curr_time = time.time()
        curr_time = 1587826117
        query = {"hashtags": {"$in": [hashtags]}, "timestamp": {"$gte": (curr_time - 60*60*24)}}
        limit = 10
        tweets = self.coll_tweets.find(query, {'_id': 0}).sort("popularity", pymongo.DESCENDING).limit(limit)
        return self.get_details_list(tweets)


    # Query to get tweets by hashtag of last week
    def hash_by_week(self, hashtags):
        # curr_time = time.time()
        curr_time = 1587826117
        query = {"hashtags": {"$in": [hashtags]}, "timestamp": {"$gte": (curr_time - 60 * 60 * 24 * 7)}}
        limit = 10
        tweets = self.coll_tweets.find(query, {'_id': 0}).sort("popularity", pymongo.DESCENDING).limit(limit)
        return self.get_details_list(tweets)


    # Query to get tweets by hashtag of last month
    def hash_by_month(self, hashtags):
        # curr_time = time.time()
        curr_time = 1587826117
        query = {"hashtags": {"$in": [hashtags]}, "timestamp": {"$gte": (curr_time - 60 * 60 * 24 * 30)}}
        limit = 10
        tweets = self.coll_tweets.find(query, {'_id': 0}).sort("popularity", pymongo.DESCENDING).limit(limit)
        return self.get_details_list(tweets)


    # Query to get tweets by text of last day
    def tweet_by_day(self, regex_pattern):
        # curr_time = time.time()
        curr_time = 1587826117
        tweets = self.coll_tweets.find({"text": {"$regex": regex_pattern, "$options": "i"},
                                        "timestamp": {"$gte": (curr_time - 60*60*24)}}, {'_id': 0}).sort(
            "popularity", pymongo.DESCENDING).limit(10)
        return self.get_details_list(tweets)


    # Query to get tweets by text of last week
    def tweet_by_week(self, regex_pattern):
        # curr_time = time.time()
        curr_time = 1587826117
        tweets = self.coll_tweets.find({"text": {"$regex": regex_pattern, "$options": "i"},
                                        "timestamp": {"$gte": (curr_time - 60*60*24*7)}}, {'_id': 0}).sort(
            "popularity", pymongo.DESCENDING).limit(10)
        return self.get_details_list(tweets)


    # Query to get tweets by text of last month
    def tweet_by_month(self, regex_pattern):
        # curr_time = time.time()
        curr_time = 1587826117
        tweets = self.coll_tweets.find({"text": {"$regex": regex_pattern, "$options": "i"},
                                        "timestamp": {"$gte": (curr_time - 60*60*24*30)}}, {'_id': 0}).sort(
            "popularity", pymongo.DESCENDING).limit(10)
        return self.get_details_list(tweets)
