# Code done by Aalap

import json
import sys
import pymongo
from datetime import datetime

# Connection to Non-Relational Database
client = pymongo.MongoClient("localhost", 27017)
db = client['twitter-covid3']

# Variable for collections
tweet_coll = db["tweets"]
comments_coll = db["comments"]


# Define a function to calculate popularity
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

line_ctr = 0
err_ctr = 0
# Read the data
with open("corona-out-3", "r") as f1:
    for line in f1:
        line_ctr += 1
        try:
            row = json.loads(line)
            # if RT is present in the tweet
            if row['text'][0:2] == 'RT':
                # Some retweets in the data do not have retweeted_status field
                if 'retweeted_status' not in row.keys():
                    continue
                data = row['retweeted_status']
                # Check if its a tweet or comment
                if data['in_reply_to_status_id_str'] is None:
                    result = tweet_coll.find_one({'id_str' : data['id_str']})
                    # Insert if the tweet does not already exist in database
                    if result is None:
                        pop = calc_popularity(data)
                        hash = []
                        if data['truncated'] is True:
                            hash_data = data['extended_tweet']['entities']['hashtags']
                        else:
                            hash_data = data['entities']['hashtags']
                        for i in hash_data:
                            hash.append(i['text'])
                        tweet = {'created_at': data['created_at'],
                                 'id_str': data['id_str'],
                                 'user_id': data['user']['id_str'],
                                 'user_name': data['user']['screen_name'],
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
                            if 'quoted_status' not in row.keys():
                                continue
                            tweet['quoted_status'] = row['quoted_status']
                        dt = datetime.strptime(data['created_at'], "%a %b %d %H:%M:%S %z %Y")
                        epoch_time = float(dt.timestamp())
                        tweet['timestamp'] = epoch_time
                        tweet_coll.insert_one(tweet)
                    else:
                        #Update Popularity
                        pop = result['popularity']
                        pop += calc_popularity(row)
                        tweet_coll.update_one({'id_str': data['id_str']}, {"$set": {"popularity": pop}})
                else:
                    result = comments_coll.find_one({'id_str': data['id_str']})
                    if result is None:
                        comment = {
                            'created_at': data['created_at'],
                            'id_str': data['id_str'],
                            'user_id': data['user']['id_str'],
                            'user_name': data['user']['screen_name'],
                            'text': data['text'],
                            'truncated': data['truncated'],
                            'is_quote_status': data['is_quote_status'],
                            'quote_count': data['quote_count'],
                            'reply_count': data['reply_count'],
                            'retweet_count': data['retweet_count'],
                            'favorite_count': data['favorite_count'],
                            'lang': data['lang'],
                            'in_reply_to_status_id_str': data['in_reply_to_status_id_str'],
                            'in_reply_to_user_id_str': data['in_reply_to_user_id_str'],
                            'in_reply_to_screen_name': data['in_reply_to_screen_name'],
                        }
                        if data['truncated'] is True:
                            comment['extended_tweet'] = data['extended_tweet']
                        if data['is_quote_status'] is True:
                            comment['quoted_status_id_str'] = data['quoted_status_id_str']
                            comment['quoted_status'] = row['quoted_status']
                        comments_coll.insert_one(comment)
            # Check if its a tweet or comment
            elif row['in_reply_to_status_id_str'] is None:
                result = tweet_coll.find_one({'id_str' : row['id_str']})
                if result is None:
                    pop = calc_popularity(row)
                    hash = []
                    if row['truncated'] is True:
                        hash_data = row['extended_tweet']['entities']['hashtags']
                    else:
                        hash_data = row['entities']['hashtags']
                    for i in hash_data:
                        hash.append(i['text'])
                    tweet = {
                        'created_at': row['created_at'],
                        'id_str': row['id_str'],
                        'user_id': row['user']['id_str'],
                        'user_name': row['user']['screen_name'],
                        'text': row['text'],
                        'truncated': row['truncated'],
                        'is_quote_status': row['is_quote_status'],
                        'quote_count': row['quote_count'],
                        'reply_count': row['reply_count'],
                        'retweet_count': row['retweet_count'],
                        'favorite_count': row['favorite_count'],
                        'lang': row['lang'],
                        'popularity': pop,
                        'hashtags': hash
                    }
                    if row['truncated'] is True:
                        tweet['extended_tweet'] = row['extended_tweet']
                    if row['is_quote_status'] is True:
                        if 'quoted_status_id_str' not in row.keys():
                            continue
                        tweet['quoted_status_id_str'] = row['quoted_status_id_str']
                        tweet['quoted_status'] = row['quoted_status']
                    dt = datetime.strptime(row['created_at'], "%a %b %d %H:%M:%S %z %Y")
                    epoch_time = float(dt.timestamp())
                    tweet['timestamp'] = epoch_time
                    tweet_coll.insert_one(tweet)
                else:
                    # Update Popularity
                    pop = result['popularity']
                    pop += calc_popularity(row)
                    tweet_coll.update_one({'id_str': row['id_str']}, {"$set": {"popularity": pop}})
            else:
                result = comments_coll.find_one({'id_str': row['id_str']})
                if result is None:
                    comment = {
                        'created_at': row['created_at'],
                        'id_str': row['id_str'],
                        'user_id': row['user']['id_str'],
                        'user_name': row['user']['screen_name'],
                        'text': row['text'],
                        'truncated': row['truncated'],
                        'is_quote_status': row['is_quote_status'],
                        'quote_count': row['quote_count'],
                        'reply_count': row['reply_count'],
                        'retweet_count': row['retweet_count'],
                        'favorite_count': row['favorite_count'],
                        'lang': row['lang'],
                        'in_reply_to_status_id_str': row['in_reply_to_status_id_str'],
                        'in_reply_to_user_id_str': row['in_reply_to_user_id_str'],
                        'in_reply_to_screen_name': row['in_reply_to_screen_name']
                    }
                    if row['truncated'] is True:
                        comment['extended_tweet'] = row['extended_tweet']
                    if row['is_quote_status'] is True:
                        comment['quoted_status_id_str'] = row['quoted_status_id_str']
                        comment['quoted_status'] = row['quoted_status']
                    comments_coll.insert_one(comment)
        except Exception as e:
            if line_ctr%2 != 0:
                err_ctr += 1
                print(line)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(exc_type, exc_tb.tb_lineno)
                if err_ctr == 1:
                    break

# Add Index on username in tweets collection
db['tweets'].create_index('user_name')
# Add Index on original tweet id on comments collection
db['comments'].create_index('in_reply_to_status_id_str')
