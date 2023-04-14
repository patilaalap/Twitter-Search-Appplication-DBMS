import pymongo
import pandas as pd

client = pymongo.MongoClient("localhost", 27017)

db = client['twitter-covid2']

tweet_coll = db["tweets"]
comments_coll = db["comments"]

covid2_df = pd.read_json('corona-out-2', lines=True)

for index, row in covid2_df.iterrows():
    # if RT is present in the retweet
    if row['text'][0:2] == 'RT':
        if row['retweeted_status']['in_reply_to_status_id_str'] is None:
            tweet = {'created_at': row['created_at'],
                     'id_str': row['id_str'],
                     'text': row['text'],
                     'truncated': row['truncated'],
                     'retweeted_status': row['retweeted_status'],
                     'quoted_status_id_str': row['quoted_status_id_str'],
                     'quoted_status': row['quoted_status'],
                     'is_quote_status': row['is_quote_status'],
                     'quote_count': row['quote_count'],
                     'reply_count': row['reply_count'],
                     'retweet_count': row['retweet_count'],
                     'favorite_count': row['favorite_count'],
                     'lang': row['lang'],
                     'extended_tweet': row['extended_tweet'],
                     'possibly_sensitive': row['possibly_sensitive']
                     }
            tweet_coll.insert_one(tweet)
        else:
            comment = {'created_at': row['created_at'],
                       'id_str': row['id_str'],
                       'text': row['text'],
                       'truncated': row['truncated'],
                       'retweeted_status': row['retweeted_status'],
                       'quoted_status_id_str': row['quoted_status_id_str'],
                       'quoted_status': row['quoted_status'],
                       'is_quote_status': row['is_quote_status'],
                       'quote_count': row['quote_count'],
                       'reply_count': row['reply_count'],
                       'retweet_count': row['retweet_count'],
                       'favorite_count': row['favorite_count'],
                       'lang': row['lang'],
                       'extended_tweet': row['extended_tweet'],
                       'possibly_sensitive': row['possibly_sensitive'],
                       'in_reply_to_status_id_str': row['in_reply_to_status_id_str'],
                       'in_reply_to_user_id_str': row['in_reply_to_user_id_str'],
                       'in_reply_to_screen_name': row['in_reply_to_screen_name']
                       }
            comments_coll.insert_one(comment)
    elif pd.isna(row['in_reply_to_status_id_str']) is True:
        tweet = {
            'created_at': row['created_at'],
            'id_str': row['id_str'],
            'text': row['text'],
            'truncated': row['truncated'],
            'retweeted_status': row['retweeted_status'],
            'quoted_status_id_str': row['quoted_status_id_str'],
            'quoted_status': row['quoted_status'],
            'is_quote_status': row['is_quote_status'],
            'quote_count': row['quote_count'],
            'reply_count': row['reply_count'],
            'retweet_count': row['retweet_count'],
            'favorite_count': row['favorite_count'],
            'lang': row['lang'],
            'extended_tweet': row['extended_tweet'],
            'possibly_sensitive': row['possibly_sensitive']
        }
        tweet_coll.insert_one(tweet)
    else:
        comment = {
            'created_at': row['created_at'],
            'id_str': row['id_str'],
            'text': row['text'],
            'truncated': row['truncated'],
            'retweeted_status': row['retweeted_status'],
            'quoted_status_id_str': row['quoted_status_id_str'],
            'quoted_status': row['quoted_status'],
            'is_quote_status': row['is_quote_status'],
            'quote_count': row['quote_count'],
            'reply_count': row['reply_count'],
            'retweet_count': row['retweet_count'],
            'favorite_count': row['favorite_count'],
            'lang': row['lang'],
            'extended_tweet': row['extended_tweet'],
            'possibly_sensitive': row['possibly_sensitive'],
            'in_reply_to_status_id_str': row['in_reply_to_status_id_str'],
            'in_reply_to_user_id_str': row['in_reply_to_user_id_str'],
            'in_reply_to_screen_name': row['in_reply_to_screen_name']
        }
        comments_coll.insert_one(comment)
# Iterate through the rows of the DataFrame and insert each row as a separate document in the collection
for index, row in covid2_df.iterrows():
    tweet = {
        'created_at': row['created_at'],
        'id_str': row['id_str'],
        'text': row['text'],
        'truncated': row['truncated'],
        'retweeted_status': row['retweeted_status'],
        'quoted_status_id_str': row['quoted_status_id_str'],
        'quoted_status': row['quoted_status'],
        'is_quote_status': row['is_quote_status'],
        'quote_count': row['quote_count'],
        'reply_count': row['reply_count'],
        'retweet_count': row['retweet_count'],
        'favorite_count': row['favorite_count'],
        'lang': row['lang'],
        'extended_tweet': row['extended_tweet'],
        'possibly_sensitive': row['possibly_sensitive']
    }
    collection.insert_one(tweet)
