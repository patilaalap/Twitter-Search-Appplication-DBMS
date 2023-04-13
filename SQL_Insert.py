import sqlite3
import pandas as pd

covid2 = pd.read_json('corona-out-2',lines = True)

df = pd.json_normalize(covid2['user'])
# adding timestamp column
df = df.assign(timestamp= covid2['timestamp_ms'])
df['timestamp'] = df['timestamp'].astype(str)

df = df.drop(['translator_type', 'protected', 'utc_offset', 'time_zone', 'geo_enabled', 'lang',
                'contributors_enabled', 'is_translator', 'profile_background_color', 'profile_background_image_url',
                'profile_background_image_url_https', 'profile_background_tile', 'profile_link_color',
                'profile_sidebar_border_color', 'profile_sidebar_fill_color', 'profile_text_color',
                'profile_use_background_image', 'profile_image_url', 'profile_image_url_https',
                'profile_banner_url', 'default_profile', 'default_profile_image', 'following',
                'follow_request_sent', 'notifications'], axis=1)

conn = sqlite3.connect('user_db.db')

for i, row in df.iterrows():
    # Define the SQL query to check if id already exists in the table
    check_query = f"""
    SELECT id, timestamp FROM user WHERE id={row['id']}
    """
    result = conn.execute(check_query).fetchone()

    # If id doesn't exist, insert the row into the table
    if not result:
        insert_query = """
        INSERT INTO user (id, id_str, name, screen_name, location, url, description, verified, followers_count,
                           friends_count, listed_count, favourites_count, statuses_count, created_at, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        conn.execute(insert_query,
                     (row['id'], row['id_str'], row['name'], row['screen_name'], row['location'], row['url'],
                      row['description'], row['verified'], row['followers_count'], row['friends_count'],
                      row['listed_count'], row['favourites_count'], row['statuses_count'], row['created_at'],
                      row['timestamp']))
        conn.commit()

    # If id already exists and the new timestamp is greater, update the row
    elif row['timestamp'] > result[1]:
        update_query = """
            UPDATE user SET id_str=?, name=?, screen_name=?, location=?, url=?, description=?, 
            verified=?, followers_count=?, friends_count=?, listed_count=?, favourites_count=?, 
            statuses_count=?, created_at=?, timestamp=?
            WHERE id=?
            """
        conn.execute(update_query, (row['id_str'], row['name'], row['screen_name'], row['location'], row['url'],
                                    row['description'], row['verified'], row['followers_count'], row['friends_count'],
                                    row['listed_count'], row['favourites_count'], row['statuses_count'],
                                    row['created_at'],
                                    row['timestamp'], row['id']))
        conn.commit()

    # If id already exists and the new timestamp is less than or equal to the old timestamp, skip the row
    else:
        continue