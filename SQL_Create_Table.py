import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('user_db.db')

"""
sql = "DROP TABLE IF EXISTS user"

# Execute the SQL query to drop the table
conn.execute(sql)

# Commit the changes and close the connection
conn.commit()
"""

# Define the SQL query to create the table
# CHECK CREATED AT FOR TYPE (DATE TIME FIELD)
sql = """
CREATE TABLE user (
    id BIGINT,
    id_str TEXT,
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
conn.execute(sql)

# Commit the changes and close the connection
conn.commit()
