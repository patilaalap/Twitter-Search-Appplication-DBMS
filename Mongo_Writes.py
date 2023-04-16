import pymongo
import pandas as pd
import numpy as np

client = pymongo.MongoClient("localhost", 27017)

db = client['twitter-covid2_updated']

tweet_coll = db["tweets"]
comments_coll = db["comments"]

covid2_df = pd.read_json('corona-out-2', lines=True)

def calc_popularity(data):
    pop = 0
    pop += data['quote_count']*20
    pop += data['reply_count']*3
    pop += data['retweet_count']*20
    pop += data['favorite_count']*5
    if data['user'] == True:
        pop += 10000
    pop += data['user']['followers_count'] * 10
    return pop

for index, row in covid2_df.iterrows():
    # if RT is present in the retweet
    if row['text'][0:2] == 'RT':
        if pd.isna(row['retweeted_status']) is True:
            continue
        data = row['retweeted_status']
        if data['in_reply_to_status_id_str'] is None:
            result = tweet_coll.find_one({'id_str' : data['id_str']})
            if result is None:
                pop = calc_popularity(data)
                hash = []
                hash_data = data['entities']['hashtags']
                for i in hash_data:
                    hash.append(i['text'])
                tweet = {'created_at': data['created_at'],
                         'id_str': data['id_str'],
                         'user_id': data['user']['id_str'],
                         'text': data['text'],
                         'truncated': data['truncated'],
                         'is_quote_status': data['is_quote_status'],
                         'quote_count': data['quote_count'],
                         'reply_count': data['reply_count'],
                         'retweet_count': data['retweet_count'],
                         'favorite_count': data['favorite_count'],
                         'lang': data['lang'],
                         'popularity': pop,
                         'hashtags': hash
                         }
                if data['truncated'] is True:
                    tweet['extended_tweet'] = data['extended_tweet']
                if data['is_quote_status'] is True:
                    tweet['quoted_status_id_str'] = data['quoted_status_id_str']
                    tweet['quoted_status'] = row['quoted_status']
                tweet_coll.insert_one(tweet)
            else:
                #Update Popularity
                pop = result['popularity']
                pop += calc_popularity(row)
                tweet_coll.update_one({'id_str': data['id_str']}, {"$set": {"popularity": pop}})
    elif pd.isna(row['in_reply_to_status_id_str']) is True:
        result = tweet_coll.find_one({'id_str' : row['id_str']})
        if result is None:
            pop = calc_popularity(row)
            hash = []
            hash_data = data['entities']['hashtags']
            for i in hash_data:
                hash.append(i['text'])
            tweet = {
                'created_at': row['created_at'],
                'id_str': row['id_str'],
                'user_id': row['user']['id_str'],
                'text': row['text'],
                'truncated': row['truncated'],
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
                'popularity': pop,
                'hashtags': hash
            }
            tweet_coll.insert_one(tweet)
        else:
            # Update Popularity
            pop = result['popularity']
            pop += calc_popularity(row)
            tweet_coll.update_one({'id_str': row['id_str']}, {"$set": {"popularity": pop}})
    else:
        comment = {
            'created_at': row['created_at'],
            'id_str': row['id_str'],
            'text': row['text'],
            'truncated': row['truncated'],
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
