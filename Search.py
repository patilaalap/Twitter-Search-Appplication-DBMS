# Code done by Aalap and Rushabh

from SQL_Read import UserDatabase
from Mongo_Read import TweetQuery
from Cache import Cache
import tkinter as tk
import re
import time

tweet_obj = TweetQuery()
user_obj = UserDatabase()
cache_obj = Cache()

# Function to clear frame of Tkinter GUI
def clear_frame():
    for widgets in frame.winfo_children():
        widgets.destroy()

"""
retrieve_input() function is invoked everytime we click on the search button.
Retrieve input function is used to extract the text from the search-box, 
then it matches the pattern with @,# and a normal text and accordingly calls the functions and prints  the output.
It also adds and retrieves data from the cache and also checks if the object is present in the cache or not."""
def retrieve_input():
    x = e1.get()
    offset = 0
    pattern = r"^@"
    pattern_hashtag = r"^#"
    clear_frame()
    if re.match(pattern,x):
        tk.Label(frame, text="Username", font=('Helveticabold', 15, "bold")).grid(row=5, column=0)
        tk.Label(frame, text="Account Name", font=('Helveticabold', 15, "bold")).grid(row=5, column=1)
        in_Cache = cache_obj.is_present_in_cache(x)
        if in_Cache == True:
            i = 0
            print("From Cache")
            start = time.time()
            y = cache_obj.retrieve_from_cache(x)
            end = time.time()
            disp = f"Time to retrieve {end - start:.10f}"
            tk.Label(frame, text=disp).grid(row=4)
            for j in range(len(y)-1):
                link = tk.Label(frame, text=y[j][1], font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link.grid(row=i + 6, column=0)
                link.bind("<Button-1>", lambda event: user_details(event))
                link = tk.Label(frame, text=y[j][0], font=('Helveticabold', 15))
                link.grid(row=i + 6, column=1)
                i = i + 1
        else:
            start = time.time()
            y = user_obj.get_user_by_name(x[1:],offset)
            end = time.time()
            disp = f"Time to retrieve {end - start:.10f}"
            tk.Label(frame, text=disp).grid(row=4)
            print("No cache")
            i = 0
            for rows in y:
                link = tk.Label(frame, text=rows[1], font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link.grid(row=i + 6, column = 0)
                link.bind("<Button-1>", lambda event: user_details(event))
                link = tk.Label(frame, text=rows[0], font=('Helveticabold', 15))
                link.grid(row=i + 6, column=1)
                i = i+1
            print(type(y))
            cache_obj.add_in_cache(x,y)
        buttonCommit = tk.Button(frame, height=1, width=10, text="Show more", command=lambda: show_more(x,offset+10))
        buttonCommit.grid()
        tk.mainloop()
    elif re.match(pattern_hashtag,x):
        # Cache
        print("# pattern")
        tk.Label(frame, text="Tweet ID", font=('Helveticabold', 15, "bold")).grid(row=5, column=0)
        tk.Label(frame, text="User Name", font=('Helveticabold', 15, "bold")).grid(row=5, column=1)
        tk.Label(frame, text="Tweet", font=('Helveticabold', 15, "bold")).grid(row=5, column=2)
        in_Cache = cache_obj.is_present_in_cache(x)
        if in_Cache == True:
            i = 0
            print("From Cache")
            start = time.time()
            y = cache_obj.retrieve_from_cache(x)
            end = time.time()
            disp = f"Time to retrieve {end - start:.10f}"
            tk.Label(frame, text=disp).grid(row=4)
            for j in range(len(y) - 1):
                t_id = y[j]['id_str']
                link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link1.grid(row=i + 6, column=0, sticky="n")
                link1.bind("<Button-1>", lambda event: tweet_details(event))
                u_name = y[j]['user_name']
                link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link2.grid(row=i + 6, column=1, sticky="n")
                link2.bind("<Button-1>", lambda event: user_details(event))
                tweet = y[j]['text']
                link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
                link3.grid(row=i + 6, column=2)
                i = i + 1
        else:
            start = time.time()
            tweets = tweet_obj.search_tweets_by_hashtags(x[1:],offset)
            end = time.time()
            disp = f"Time to retrieve {end - start:.10f}"
            tk.Label(frame, text=disp).grid(row=4)
            i = 0
            for rows in tweets:
                t_id = rows['id_str']
                link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link1.grid(row=i + 6, column=0, sticky="n")
                link1.bind("<Button-1>", lambda event: tweet_details(event))
                u_name = rows['user_name']
                link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link2.grid(row=i + 6, column=1, sticky="n")
                link2.bind("<Button-1>", lambda event: user_details(event))
                tweet = rows['text']
                link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
                link3.grid(row=i + 6, column=2)
                i = i + 1
            print(type(tweets))
            cache_obj.add_in_cache(x, tweets)
        buttonCommit = tk.Button(frame, height=1, width=10, text="Show more", command=lambda: show_more_hashtags(x,offset+10))
        buttonCommit.grid()
        buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10hashtag_day(x))
        buttonCommit.grid(row = i+6,column=0)
        buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10hashtag_week(x))
        buttonCommit.grid(row = i+6,column=1)
        buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10hashtag_month(x))
        buttonCommit.grid(row=i+6,column=2)
        tk.mainloop()
    else:
        tk.Label(frame, text="Tweet ID", font=('Helveticabold', 15, "bold")).grid(row=5, column=0)
        tk.Label(frame, text="User Name", font=('Helveticabold', 15, "bold")).grid(row=5, column=1)
        tk.Label(frame, text="Tweet", font=('Helveticabold', 15, "bold")).grid(row=5, column=2)
        in_Cache = cache_obj.is_present_in_cache(x)
        if in_Cache == True:
            i = 0
            print("From Cache")
            start = time.time()
            y = cache_obj.retrieve_from_cache(x)
            end = time.time()
            disp = f"Time to retrieve {end - start:.10f}"
            tk.Label(frame, text=disp).grid(row=4)
            for j in range(len(y) - 1):
                t_id = y[j]['id_str']
                link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link1.grid(row=i + 6, column=0, sticky="n")
                link1.bind("<Button-1>", lambda event: tweet_details(event))
                u_name = y[j]['user_name']
                link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link2.grid(row=i + 6, column=1, sticky="n")
                link2.bind("<Button-1>", lambda event: user_details(event))
                tweet = y[j]['text']
                link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
                link3.grid(row=i + 6, column=2)
                i = i + 1
        else:
            i = 0
            start = time.time()
            tweets = tweet_obj.query_tweets_by_regex(x,offset)
            end = time.time()
            disp = f"Time to retrieve {end - start:.10f}"
            tk.Label(frame, text=disp).grid(row=4)
            for rows in tweets:
                t_id = rows['id_str']
                link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link1.grid(row=i + 6, column=0, sticky="n")
                link1.bind("<Button-1>", lambda event: tweet_details(event))
                u_name = rows['user_name']
                link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link2.grid(row=i + 6, column=1, sticky="n")
                link2.bind("<Button-1>", lambda event: user_details(event))
                tweet = rows['text']
                link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
                link3.grid(row=i + 6, column=2)
                i = i + 1
            cache_obj.add_in_cache(x, tweets)
        buttonCommit = tk.Button(frame, height=1, width=10, text="Show more", command=lambda: show_more_tweets(x,offset+10))
        buttonCommit.grid()
        buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10tweet_day(x))
        buttonCommit.grid(row=i + 6, column=0)
        buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10tweet_week(x))
        buttonCommit.grid(row=i + 6, column=1)
        buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10tweet_month(x))
        buttonCommit.grid(row=i + 6, column=2)
        tk.mainloop()


# This function filters out a particular searched hashtag by a DAY and displays the top tweets
def top_10hashtag_day(x):
    clear_frame()
    start = time.time()
    tweets = tweet_obj.hash_by_day(x[1:])
    end = time.time()
    disp = f"Time to retrieve {end - start:.10f}"
    tk.Label(frame, text=disp).grid(row=4)
    i = 0
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 6, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 6, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 6, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10hashtag_day(x))
    buttonCommit.grid(row=i + 6, column=0)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10hashtag_week(x))
    buttonCommit.grid(row=i + 6, column=1)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10hashtag_month(x))
    buttonCommit.grid(row=i + 6, column=2)
    tk.mainloop()

# This function filters out a particular searched hashtag by MONTH and displays the top tweets
def top_10hashtag_month(x):
    clear_frame()
    start = time.time()
    tweets = tweet_obj.hash_by_month(x[1:])
    end = time.time()
    disp = f"Time to retrieve {end - start:.10f}"
    tk.Label(frame, text=disp).grid(row=4)
    i = 0
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 6, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 6, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 6, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10hashtag_day(x))
    buttonCommit.grid(row=i + 6, column=0)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10hashtag_week(x))
    buttonCommit.grid(row=i + 6, column=1)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10hashtag_month(x))
    buttonCommit.grid(row=i + 6, column=2)
    tk.mainloop()

# This function filters out a particular searched hashtag by WEEK and displays the top tweets
def top_10hashtag_week(x):
    clear_frame()
    start = time.time()
    tweets = tweet_obj.hash_by_week(x[1:])
    end = time.time()
    disp = f"Time to retrieve {end - start:.10f}"
    tk.Label(frame, text=disp).grid(row=4)
    i = 0
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 6, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 6, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 6, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10hashtag_day(x))
    buttonCommit.grid(row=i + 6, column=0)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10hashtag_week(x))
    buttonCommit.grid(row=i + 6, column=1)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10hashtag_month(x))
    buttonCommit.grid(row=i + 6, column=2)
    tk.mainloop()

# This function filters out a particular searched text by a DAY and displays the top tweets
def top_10tweet_day(x):
    clear_frame()
    i = 0
    start = time.time()
    tweets = tweet_obj.tweet_by_day(x)
    end = time.time()
    disp = f"Time to retrieve {end - start:.10f}"
    tk.Label(frame, text=disp).grid(row=4)
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 6, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 6, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 6, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10tweet_day(x))
    buttonCommit.grid(row=i + 6, column=0)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10tweet_week(x))
    buttonCommit.grid(row=i + 6, column=1)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10tweet_month(x))
    buttonCommit.grid(row=i + 6, column=2)
    tk.mainloop()

# This function filters out a particular searched text by WEEK and displays the top tweets
def top_10tweet_week(x):
    clear_frame()
    i = 0
    start = time.time()
    tweets = tweet_obj.tweet_by_week(x)
    end = time.time()
    disp = f"Time to retrieve {end - start:.10f}"
    tk.Label(frame, text=disp).grid(row=4)
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 6, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 6, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 6, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10tweet_day(x))
    buttonCommit.grid(row=i + 6, column=0)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10tweet_week(x))
    buttonCommit.grid(row=i + 6, column=1)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10tweet_month(x))
    buttonCommit.grid(row=i + 6, column=2)
    tk.mainloop()

# This function filters out a particular searched text by MONTH and displays the top tweets
def top_10tweet_month(x):
    clear_frame()
    i = 0
    start = time.time()
    tweets = tweet_obj.tweet_by_month(x)
    end = time.time()
    disp = f"Time to retrieve {end - start:.10f}"
    tk.Label(frame, text=disp).grid(row=4)
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 6, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 6, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 6, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10tweet_day(x))
    buttonCommit.grid(row=i + 6, column=0)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10tweet_week(x))
    buttonCommit.grid(row=i + 6, column=1)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10tweet_month(x))
    buttonCommit.grid(row=i + 6, column=2)
    tk.mainloop()

# This function retrieves and displays all the user_details of a particular user.
def user_details(event):
    clicked_label = event.widget
    label_text = clicked_label.cget("text")
    clear_frame()
    user_det = user_obj.get_userdetails(label_text)
    for rows in user_det:
        disp = "Name : "+rows[0]+"\nUsername : "+rows[1]+"\n Followers : "+str(rows[4])+\
               "   Following : "+str(rows[5])+"\nCreated at : "+str(rows[6])+"\n\n\nDescription : "+rows[3]
        tk.Label(frame, text=disp).grid(row=2)
        tk.Button(frame, height=1, width=10, text="Get Tweets", command=lambda : user_tweets(rows[1])).grid(row=3)
    tk.mainloop()

"""This function retrieves and displays all the tweet details of a particular tweet and also gives 
a button to check sentiment of the tweet."""
def tweet_details(event):
    clicked_label = event.widget
    label_text = clicked_label.cget("text")
    clear_frame()
    tweet_det = tweet_obj.get_tweet_details(label_text)
    for rows in tweet_det:
        link1 = tk.Label(frame, text=rows['user_name'], font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=5, column=0)
        link1.bind("<Button-1>", lambda event: user_details(event))
        if rows['truncated'] is True:
            tk.Label(frame, text=rows['extended_tweet']['full_text'], font=('Helveticabold', 14)).grid(row=5, column=1)
        else:
            tk.Label(frame, text=rows['text'], font=('Helveticabold', 15)).grid(row=5, column=1)
        disp = "Likes: "+str(rows['favorite_count']) + " Retweets: " + str(rows['retweet_count']) +\
               " Comments: " + str(rows['reply_count'])
        tk.Label(frame, text=disp, font=('Helveticabold', 15)).grid(row=6, column=1)
        if rows['is_quote_status'] is True:
            link1 = tk.Label(frame, text=rows['quoted_status']['user']['screen_name'], font=('Helveticabold', 15),
                             fg="blue", cursor="hand2")
            link1.grid(row=7, column=0)
            link1.bind("<Button-1>", lambda event: user_details(event))
            link2 = tk.Label(frame, text=rows['quoted_status']['id_str'], font=('Helveticabold', 15),
                             fg="blue", cursor="hand2")
            link2.grid(row=8, column=0)
            link2.bind("<Button-1>", lambda event: tweet_details(event))
            tk.Label(frame, text=rows['quoted_status']['text'], font=('Helveticabold', 15), borderwidth=1,
                     relief="sunken").grid(row=8, column=1, sticky="w")
            i = 9
        else:
            i = 7
        button1 = tk.Button(frame, height=1, width=10, text="Retweets",
                            command=lambda: display_retweets(rows['id_str'], i+3))
        button1.grid(row = i, column=1)
        button2 = tk.Button(frame, height=1, width=10, text="Comments",
                            command=lambda: display_comments(rows['id_str'], i+3))
        button2.grid(row=i+1, column=1)
        buttonCommit = tk.Button(frame, height=1, width=10, text="Get Sentiment", command=lambda: get_sentiment(label_text))
        buttonCommit.grid(row=i+2, column = 1)
    tk.mainloop()

# This function is invoked on clicking the GET SENTIMENT button and gives the sentiment of that particular tweet
def get_sentiment(label_text):
    print("Sentiment")
    y = tweet_obj.get_sentiment(label_text)
    for rows in y:
        link1 = tk.Label(frame, text=rows['sentiment'], font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(column = 1)
    tk.mainloop()

# This function is invoked on clicking the show more button which loads the next 10 users of a particular search
def show_more(x,offset):
    clear_frame()
    y = user_obj.get_user_by_name(x[1:], offset)
    i = 0
    tk.Label(frame, text="Username", font=('Helveticabold', 15, "bold")).grid(row=4, column=0)
    tk.Label(frame, text="Account Name", font=('Helveticabold', 15, "bold")).grid(row=4, column=1)
    for rows in y:
        link = tk.Label(frame, text=rows[1], font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link.grid(row=i + 5, column=0)
        link.bind("<Button-1>", lambda event: user_details(event))
        link = tk.Label(frame, text=rows[0], font=('Helveticabold', 15))
        link.grid(row=i + 5, column=1)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="Show more", command=lambda: show_more(x, offset + 10))
    buttonCommit.grid()
    tk.mainloop()


# This function is invoked on clicking the show more button which loads the next 10 results of a particular hashtag
def show_more_hashtags(x,offset):
    clear_frame()
    tk.Label(frame, text="Tweet ID", font=('Helveticabold', 15, "bold")).grid(row=5, column=0)
    tk.Label(frame, text="User Name", font=('Helveticabold', 15, "bold")).grid(row=5, column=1)
    tk.Label(frame, text="Tweet", font=('Helveticabold', 15, "bold")).grid(row=5, column=2)
    start = time.time()
    tweets = tweet_obj.search_tweets_by_hashtags(x[1:],offset)
    end = time.time()
    disp = f"Time to retrieve {end - start:.10f}"
    tk.Label(frame, text=disp).grid(row=4)
    i = 0
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 6, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 6, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 6, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="Show more", command=lambda: show_more_hashtags(x, offset + 10))
    buttonCommit.grid()
    tk.mainloop()

# This function is invoked on clicking the show more button which loads the next 10 tweets of a particular text search
def show_more_tweets(x,offset):
    clear_frame()
    tk.Label(frame, text="Tweet ID", font=('Helveticabold', 15, "bold")).grid(row=5, column=0)
    tk.Label(frame, text="User Name", font=('Helveticabold', 15, "bold")).grid(row=5, column=1)
    tk.Label(frame, text="Tweet", font=('Helveticabold', 15, "bold")).grid(row=5, column=2)
    i = 0
    start = time.time()
    tweets = tweet_obj.query_tweets_by_regex(x,offset)
    end = time.time()
    disp = f"Time to retrieve {end - start:.10f}"
    tk.Label(frame, text=disp).grid(row=4)
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 6, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 6, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 6, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="Show more",command=lambda: show_more_tweets(x, offset + 10))
    buttonCommit.grid()
    tk.mainloop()


# This function retrieves and displays the top 10 Users from the entire database
def top_10_users():
    y = user_obj.get_top_ten()
    i = 0
    clear_frame()
    tk.Label(frame, text="User Name", font=('Helveticabold', 15, "bold")).grid(row=4, column=0)
    tk.Label(frame, text="Account Name", font=('Helveticabold', 15, "bold")).grid(row=4, column=1)
    for rows in y:
        link = tk.Label(frame, text=rows[1], font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link.grid(row=i + 5, column=0)
        link.bind("<Button-1>", lambda event: user_details(event))
        link = tk.Label(frame, text=rows[0], font=('Helveticabold', 15))
        link.grid(row=i + 5, column=1)
        i = i + 1
    tk.mainloop()


# This function retrieves and displays top 10 tweets from the entire database.
def top_10_tweets():
    clear_frame()
    tweets = tweet_obj.get_top_10_popular_tweets()
    i = 0
    tk.Label(frame, text="Tweet ID", font=('Helveticabold', 15, "bold")).grid(row=4, column=0)
    tk.Label(frame, text="User Name", font=('Helveticabold', 15, "bold")).grid(row=4, column=1)
    tk.Label(frame, text="Tweet", font=('Helveticabold', 15, "bold")).grid(row=4, column=2)
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 5, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 5, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 5, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="By day",command=lambda: top_10_day())
    buttonCommit.grid(row = i+5,column = 0)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10_week())
    buttonCommit.grid(row=i + 5, column=1)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10_month())
    buttonCommit.grid(row=i + 5, column=2)
    tk.mainloop()


# On clicking the By day button , this function displays top 10 tweets of a particular DAY
def top_10_day():
    clear_frame()
    tweets = tweet_obj.top10_by_day()
    i = 0
    tk.Label(frame, text="Tweet ID", font=('Helveticabold', 15, "bold")).grid(row=4, column=0)
    tk.Label(frame, text="User Name", font=('Helveticabold', 15, "bold")).grid(row=4, column=1)
    tk.Label(frame, text="Tweet", font=('Helveticabold', 15, "bold")).grid(row=4, column=2)
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 5, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 5, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 5, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10_day())
    buttonCommit.grid(row=i + 5, column=0)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10_week())
    buttonCommit.grid(row=i + 5, column=1)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10_month())
    buttonCommit.grid(row=i + 5, column=2)
    tk.mainloop()


# On clicking the By month button , this function displays top 10 tweets of a particular MONTH
def top_10_month():
    print("Top 10 by month")
    clear_frame()
    tweets = tweet_obj.top10_by_month()
    i = 0
    tk.Label(frame, text="Tweet ID", font=('Helveticabold', 15, "bold")).grid(row=4, column=0)
    tk.Label(frame, text="User Name", font=('Helveticabold', 15, "bold")).grid(row=4, column=1)
    tk.Label(frame, text="Tweet", font=('Helveticabold', 15, "bold")).grid(row=4, column=2)
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 5, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 5, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 5, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10_day())
    buttonCommit.grid(row=i + 5, column=0)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10_week())
    buttonCommit.grid(row=i + 5, column=1)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10_month())
    buttonCommit.grid(row=i + 5, column=2)
    tk.mainloop()


# On clicking the By week button , this function displays top 10 tweets of a particular WEEK
def top_10_week():
    print("Top 10 by week")
    clear_frame()
    tweets = tweet_obj.top10_by_week()
    i = 0
    tk.Label(frame, text="Tweet ID", font=('Helveticabold', 15, "bold")).grid(row=4, column=0)
    tk.Label(frame, text="User Name", font=('Helveticabold', 15, "bold")).grid(row=4, column=1)
    tk.Label(frame, text="Tweet", font=('Helveticabold', 15, "bold")).grid(row=4, column=2)
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 5, column=0, sticky="n")
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 5, column=1, sticky="n")
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 5, column=2)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="By day", command=lambda: top_10_day())
    buttonCommit.grid(row=i + 5, column=0)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By week", command=lambda: top_10_week())
    buttonCommit.grid(row=i + 5, column=1)
    buttonCommit = tk.Button(frame, height=1, width=10, text="By month", command=lambda: top_10_month())
    buttonCommit.grid(row=i + 5, column=2)
    tk.mainloop()


# This function retrieves all the tweets of a particular user
def user_tweets(uname):
    tweets = tweet_obj.get_tweets_by_username(uname)
    clear_frame()
    i = 0
    tk.Label(frame, text="Tweet ID", font=('Helveticabold', 15, "bold")).grid(row=4, column=0)
    tk.Label(frame, text="User Name", font=('Helveticabold', 15, "bold")).grid(row=4, column=1)
    tk.Label(frame, text="Tweet", font=('Helveticabold', 15, "bold")).grid(row=4, column=2)
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 5, column=0)
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 5, column=1)
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 5, column=2)
        i = i + 1
    tk.mainloop()


# This function is used to display comments of a particular tweet.
def display_comments(uid, i):
    comments = tweet_obj.get_comments_for_tweet(uid)
    tk.Label(frame, text="Comments", font=('Helveticabold', 15, "bold")).grid(row=i, column=1)
    i += 1
    for rows in comments:
        link1 = tk.Label(frame, text=rows['user_name'], font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i, column=0)
        link1.bind("<Button-1>", lambda event: user_details(event))
        tk.Label(frame, text=rows['text']).grid(row=i, column=1)
        i += 1


# This function is used to display the users who have retweeted a particular tweet
def display_retweets(tid, i):
    retweets = user_obj.retweets(tid)
    tk.Label(frame, text="Users who retweeted", font=('Helveticabold', 15, "bold")).grid(row=i, column=1)
    i += 1
    for rows in retweets:
        link1 = tk.Label(frame, text=rows[0], font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i, column=1)
        link1.bind("<Button-1>", lambda event: user_details(event))
        i += 1


master = tk.Tk()
master.title('Twitter search application')
master.geometry("1920x1080")
tk.Label(master, height=1, text='Search').grid(row=0)
e1 = tk.Entry(master)
e1.grid(row=1)
buttonCommit = tk.Button(master, height=1, width=10, text="Search", command=lambda: retrieve_input())
buttonCommit.grid(row=2)
buttonCommit = tk.Button(master, height=1, width=10, text="Top 10 Users", command=lambda: top_10_users())
buttonCommit.grid(row=3,column =0)
buttonCommit = tk.Button(master, height=1, width=10, text="Top 10 Tweets", command=lambda: top_10_tweets())
buttonCommit.grid(row=3,column =1)
frame = tk.Frame(master, height=1, width=10)
frame.grid(row=4)
tk.mainloop()
