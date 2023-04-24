import pymongo
import re

class TweetQuery:
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["twitter-covid2_updated"]
        self.coll_tweets = self.db["tweets"]
        self.coll_comments = self.db["comments"]

    def query_tweets_by_regex(self, regex_pattern):
        # Query tweets that match the regex pattern in the text field, ordered by popularity, and limit the results by 10
        tweets = self.coll_tweets.find({"text": {"$regex": regex_pattern, "$options": "i"}}).sort("popularity", pymongo.DESCENDING).limit(10)
        return self.get_details_list(tweets)

    def search_tweets_by_hashtags(self, hashtags):
        query = {"hashtags": {"$in": [hashtags]}}
        limit = 10
        tweets = self.coll_tweets.find(query).sort("popularity", pymongo.DESCENDING).limit(limit)
        return self.get_details_list(tweets)

    def get_tweet_details(self, tweet_id):
        tweet = self.coll_tweets.find({"id_str": tweet_id})
        return self.get_details_list(tweet)

    def get_comments_for_tweet(self, tweet_id):
        comments = self.coll_comments.find({"in_reply_to_status_id_str": tweet_id}).sort("created_at", pymongo.ASCENDING)
        return self.get_details_list(comments)

    def get_tweets_by_username(self, username):
        tweets = self.coll_tweets.find({"user_name": username})
        return self.get_details_list(tweets)

    def get_top_10_popular_tweets(self):
        top_tweets = self.coll_tweets.find().sort("popularity", pymongo.DESCENDING).limit(10)
        return self.get_details_list(top_tweets)
    def get_details_list(self, result):
        L= []
        for detail in result:
            L.append(detail)
        return L

    def get_sentiment(self,tweet_id):
        sentiment = self.coll_tweets.find({"id_str": tweet_id},{"sentiment":1,"_id":0})
        return self.get_details_list(sentiment)


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





