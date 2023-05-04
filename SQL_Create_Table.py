# Code done by Neeti

import pymysql

# establish connection to MySQL database
conn = pymysql.connect(user='root',
                              password='#Aalap21',
                              host='localhost',
                              database = 'user_db',
                              )

cursor = conn.cursor()

# SQL query to create the user table
sql = """
CREATE TABLE user (
    id_str VARCHAR(255) PRIMARY KEY,
    name TEXT,
    screen_name TEXT,
    location TEXT,
    url TEXT,
    description TEXT,
    verified BOOLEAN,
    followers_count BIGINT,
    friends_count BIGINT,
    listed_count BIGINT,
    favourites_count BIGINT,
    statuses_count BIGINT,
    created_at TEXT,
    timestamp TEXT
);
"""

# Execute the SQL query to create the table
cursor.execute(sql)

# Creating the retweets table
sql = """
CREATE TABLE retweets (
    id_str VARCHAR(255),
    original_tweet_id TEXT,
    user_id_str VARCHAR(255),
    screen_name TEXT
);
"""

# Execute the SQL query to create the table
cursor.execute(sql)

# Commit the changes
conn.commit()
