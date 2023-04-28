from Mongo_Writes import tweet_coll
import pymongo
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob

# defining the stop words using nltk library
stop_words = set(stopwords.words('english'))

for tweet in tweet_coll.find():
    # If tweet is truncated, use the full_text field of the extended_text object for sentiment analysis
    if tweet['truncated'] == True:
        text = tweet['extended_tweet']['full_text']
    # Otherwise use the text of the tweet
    else:
        text = tweet['text']
    # Removing the stop words and splitting the text
    words = [w for w in text.lower().split() if not w in stop_words]

    # Joining the words again
    text = ' '.join(words)
    blob = TextBlob(text)
    # Giving a polarity score to the tweets
    score = round(blob.sentiment.polarity, 2)
    # Setting a sentiment according to the polarity
    sentiment = 'Neutral'
    if score >= 0.35:
        sentiment = 'Positive'
    elif score <= -0.35:
        sentiment = 'Negative'
    # Updating the tweets collection
    tweet_coll.update_one({'_id': tweet['_id']}, {'$set': {'sentiment': sentiment, 'score': score}})
