from Mongo_Writes import tweet_coll
import pymongo
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob

stop_words = set(stopwords.words('english'))

for tweet in tweet_coll.find():
    if tweet['truncated'] == True:
        text = tweet['extended_tweet']['full_text']
    else:
        text = tweet['text']

    words = [w for w in text.lower().split() if not w in stop_words]

    text = ' '.join(words)
    blob = TextBlob(text)
    score = round(blob.sentiment.polarity, 2)
    sentiment = 'Neutral'
    if score >= 0.35:
        sentiment = 'Positive'
    elif score <= -0.35:
        sentiment = 'Negative'

    tweet_coll.update_one({'_id': tweet['_id']}, {'$set': {'sentiment': sentiment, 'score': score}})
