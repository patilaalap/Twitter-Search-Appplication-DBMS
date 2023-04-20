import pymongo
import re

class TweetQuery:
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["twitter-covid2_updated"]
        self.collection = self.db["tweets"]
        self.collection = self.db["comments"]

    def query_tweets_by_regex(self, regex_pattern):
        # Query tweets that match the regex pattern in the text field, ordered by popularity, and limit the results by 10
        tweets = self.collection.find({"text": {"$regex": regex_pattern, "$options": "i"}},{'text':1,'id_str':1, '_id':0}).sort("popularity", pymongo.DESCENDING).limit(10)
        return self.get_details_list(tweets)

    def search_tweets_by_hashtags(self, hashtags):
        query = {"hashtags": {"$in": [hashtags]}}
        limit = 10
        tweets = self.collection.find(query,{'text':1,'_id':0}).sort("popularity", pymongo.DESCENDING).limit(limit)
        return self.get_details_list(tweets)

    def get_tweet_details(self, tweet_id):
        tweet = self.collection.find_one({"id_str": tweet_id})
        return self.get_details_list(tweet)

    def get_comments_for_tweet(self, tweet_id):
        comments = self.collection.find({"in_reply_to_status_id_str": tweet_id}).sort("created_at", pymongo.ASCENDING)
        return self.get_details_list(comments)

    def get_tweets_by_username(self, username):
        tweets = self.collection.find({"user_name": username})
        return self.get_details_list(tweets)

    def get_top_10_popular_tweets(self):
        top_tweets = self.collection.find().sort("popularity", pymongo.DESCENDING).limit(10)
        for tweet in top_tweets:
            print(tweet)
    def get_details_list(self, result):
        L= []
        for detail in result:
            L.append(detail)
        return L


#Constructor calling
#tweet_query = TweetQuery()

#Example Regex Pattern
#regex_pattern = input("Enter the regex pattern: ")
#limit = 10
#tweets = tweet_query.query_tweets_by_regex(regex_pattern)
#print(type(tweets))
#print(tweets)
#tweet_query.print_tweets_regex(tweets)




#hashtag = TweetQuery_Hashtag()
#hashtags = input("Enter the hashtag pattern: ")
#limit = 10
#tweets = hashtag.search_tweets_by_hashtags(hashtags)
#print(type(tweets))
#hashtag.print_tweets(tweets)
#print(tweets)
#tweet_query.print_tweets_regex(tweets)





