from SQL_Read import UserDatabase
from Mongo_Read import TweetQuery
from Cache import Cache

import tkinter as tk
import re


tweet_obj = TweetQuery()
user_obj = UserDatabase()
cache_obj = Cache()


def clear_frame():
    for widgets in frame.winfo_children():
        widgets.destroy()


def retrieve_input():
    x = e1.get()
    offset = 0
    pattern = r"^@"
    pattern_hashtag = r"^#"
    clear_frame()
    if re.match(pattern,x):
        in_Cache = cache_obj.is_present_in_cache(x[1:])
        if in_Cache == True:
            i = 0
            print("From Cache")
            y = cache_obj.retrieve_from_cache(x[1:])
            for j in range(len(y)-1):
                link = tk.Label(frame, text=y[j][1], font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link.grid(row=i + 4, column=0)
                link.bind("<Button-1>", lambda event: user_details(event))
                link = tk.Label(frame, text=y[j][0], font=('Helveticabold', 15))
                link.grid(row=i + 4, column=1)
                i = i + 1
        else:
            y = user_obj.get_user_by_name(x[1:],offset)
            print("No cache")
            i = 0
            for rows in y:
                link = tk.Label(frame, text=rows[1], font=('Helveticabold', 15), fg="blue", cursor="hand2")
                link.grid(row=i + 4, column = 0)
                link.bind("<Button-1>", lambda event: user_details(event))
                link = tk.Label(frame, text=rows[0], font=('Helveticabold', 15))
                link.grid(row=i + 4, column=1)
                i = i+1
            cache_obj.add_in_cache(x[1:],y)
        buttonCommit = tk.Button(frame, height=1, width=10, text="Show more", command=lambda: show_more(x,offset+10))
        buttonCommit.grid()
        tk.mainloop()
    elif re.match(pattern_hashtag,x):
        # Cache
        print("# pattern")
        tweets = tweet_obj.search_tweets_by_hashtags(x[1:])
        i = 0
        for rows in tweets:
            t_id = rows['id_str']
            link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
            link1.grid(row=i + 4, column=0)
            link1.bind("<Button-1>", lambda event: tweet_details(event))
            u_name = rows['user_name']
            link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
            link2.grid(row=i + 4, column=1)
            link2.bind("<Button-1>", lambda event: user_details(event))
            tweet = rows['text']
            link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
            link3.grid(row=i + 4, column=2)
            i = i + 1
        # cache_obj.add_in_cache(x[1:], y)
        # buttonCommit = tk.Button(frame, height=1, width=10, text="Show more", command=lambda: show_more(x, offset + 10))
        # buttonCommit.grid()
        tk.mainloop()
    else:
        # Cache
        tweets = tweet_obj.query_tweets_by_regex(x)
        i = 0
        for rows in tweets:
            t_id = rows['id_str']
            link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
            link1.grid(row=i + 4, column=0)
            link1.bind("<Button-1>", lambda event: tweet_details(event))
            u_name = rows['user_name']
            link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
            link2.grid(row=i + 4, column=1)
            link2.bind("<Button-1>", lambda event: user_details(event))
            tweet = rows['text']
            link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
            link3.grid(row=i + 4, column=2)

            i = i + 1
        #cache_obj.add_in_cache(x[1:], y)
        #buttonCommit = tk.Button(frame, height=1, width=10, text="Show more", command=lambda: show_more(x, offset + 10))
        #buttonCommit.grid()
        tk.mainloop()


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


def tweet_details(event):
    clicked_label = event.widget
    label_text = clicked_label.cget("text")
    clear_frame()
    tweet_det = tweet_obj.get_tweet_details(label_text)
    for rows in tweet_det:
        link1 = tk.Label(frame, text=rows['user_name'], font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=2, column=0)
        link1.bind("<Button-1>", lambda event: user_details(event))
        if rows['truncated'] is True:
            tk.Label(frame, text=rows['extended_tweet']['full_text'], font=('Helveticabold', 15)).grid(row=2, column=1)
        else:
            tk.Label(frame, text=rows['text'], font=('Helveticabold', 15)).grid(row=2, column=1)
        disp = "Likes: "+str(rows['favorite_count']) + " Retweets: " + str(rows['retweet_count']) +\
               " Comments: " + str(rows['reply_count'])
        tk.Label(frame, text=disp, font=('Helveticabold', 15)).grid(row=3, column=1)
        if rows['is_quote_status'] is True:
            tk.Label(frame, text="Quote", font=('Helveticabold', 15)).grid(row=4)
            display_comments(rows['id_str'], 5)
        else:
            display_comments(rows['id_str'], 4)
    buttonCommit = tk.Button(frame, height=1, width=10, text="Get Sentiment", command=lambda: get_sentiment(label_text))
    buttonCommit.grid(column = 1)
    tk.mainloop()

def get_sentiment(label_text):
    print("Sentiment")
    y = tweet_obj.get_sentiment(label_text)
    for rows in y:
        link1 = tk.Label(frame, text=rows['sentiment'], font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(column = 1)
    tk.mainloop()


def show_more(x,offset):
    clear_frame()
    y = user_obj.get_user_by_name(x[1:], offset)
    i = 0
    for rows in y:
        uname = rows[1]
        link = tk.Label(frame, text=rows[1], font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link.grid(row=i + 3, column=0)
        link.bind("<Button-1>", lambda event: user_details(event))
        link = tk.Label(frame, text=rows[0], font=('Helveticabold', 15))
        link.grid(row=i + 3, column=1)
        i = i + 1
    buttonCommit = tk.Button(frame, height=1, width=10, text="Show more", command=lambda: show_more(x, offset + 10))
    buttonCommit.grid()
    tk.mainloop()


def top_10_users():
    y = user_obj.get_top_ten()
    i = 0
    clear_frame()
    for rows in y:
        link = tk.Label(frame, text=rows[1], font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link.grid(row=i + 4, column=0)
        link.bind("<Button-1>", lambda event: user_details(event))
        link = tk.Label(frame, text=rows[0], font=('Helveticabold', 15))
        link.grid(row=i + 4, column=1)
        i = i + 1
    tk.mainloop()


def top_10_tweets():
    clear_frame()
    tweets = tweet_obj.get_top_10_popular_tweets()
    i = 0
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 4, column=0)
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 4, column=1)
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 4, column=2)
        i = i + 1
def user_tweets(uname):
    tweets = tweet_obj.get_tweets_by_username(uname)
    clear_frame()
    i = 0
    for rows in tweets:
        t_id = rows['id_str']
        link1 = tk.Label(frame, text=t_id, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.grid(row=i + 4, column=0)
        link1.bind("<Button-1>", lambda event: tweet_details(event))
        u_name = rows['user_name']
        link2 = tk.Label(frame, text=u_name, font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.grid(row=i + 4, column=1)
        link2.bind("<Button-1>", lambda event: user_details(event))
        tweet = rows['text']
        link3 = tk.Label(frame, text=tweet, font=('Helveticabold', 15))
        link3.grid(row=i + 4, column=2)

        i = i + 1
    tk.mainloop()

def display_comments(uid, i):
    comments = tweet_obj.get_comments_for_tweet(uid)
    print(uid)
    for rows in comments:
        tk.Label(frame, text=rows['user_name'], fg="blue").grid(row=i, column=1)
        tk.Label(frame, text=rows['text']).grid(row=i, column=2)
        i += 1

master = tk.Tk()
master.title('Twitter search application')
master.geometry("1920x1080")
tk.Label(master, text='Search').grid(row=0)
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
