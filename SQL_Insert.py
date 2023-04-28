import json
import sys
import pymysql

# establish connection to database
conn = pymysql.connect(user='root',
                              password='#Aalap21',
                              host='localhost',
                              database = 'user_db',
                              )
cursor = conn.cursor()

line_ctr = 0
with open("corona-out-3", "r") as f1:
    for line in f1:
        line_ctr += 1
        try:
            data = json.loads(line)
            row = data['user']
            # Define the SQL query to check if id already exists in the table
            check_query = f"""
            SELECT id_str, timestamp FROM user WHERE id_str={row['id_str']}
            """
            cursor.execute(check_query)
            result = cursor.fetchone()

            # If id doesn't exist, insert the row into the table
            if result is None:
                insert_query = """
                INSERT INTO user (id_str, name, screen_name, location, url, description, verified, followers_count,
                                 friends_count, listed_count, favourites_count, statuses_count, created_at, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query,
                             (row['id_str'], row['name'], row['screen_name'], row['location'], row['url'],
                              row['description'], row['verified'], row['followers_count'], row['friends_count'],
                              row['listed_count'], row['favourites_count'], row['statuses_count'], row['created_at'],
                              data['timestamp_ms']))
                #cursor.commit()

            # If id already exists and the new timestamp is greater, update the row
            elif data['timestamp_ms'] > result[1]:
                update_query = """
                    UPDATE user SET id_str=%s, name=%s, screen_name=%s, location=%s, url=%s, description=%s, 
                    verified=%s, followers_count=%s, friends_count=%s, listed_count=%s, favourites_count=%s, 
                    statuses_count=%s, created_at=%s, timestamp=%s
                    WHERE id_str=%s
                    """
                cursor.execute(update_query, (row['id_str'], row['name'], row['screen_name'], row['location'], row['url'],
                                            row['description'], row['verified'], row['followers_count'], row['friends_count'],
                                            row['listed_count'], row['favourites_count'], row['statuses_count'],
                                            row['created_at'],
                                            data['timestamp_ms'], row['id_str']))
                #conn.commit()

            # If id already exists and the new timestamp is less than or equal to the old timestamp, skip the row
            if 'retweeted_status' in data.keys():
                row = data['retweeted_status']['user']
                # Define the SQL query to check if id already exists in the table
                check_query = f"""
                            SELECT id_str, timestamp FROM user WHERE id_str={row['id_str']}
                            """
                cursor.execute(check_query)
                result = cursor.fetchone()

                # If id doesn't exist, insert the row into the table
                if result is None:
                    insert_query = """
                                INSERT INTO user (id_str, name, screen_name, location, url, description, verified, followers_count,
                                                 friends_count, listed_count, favourites_count, statuses_count, created_at, timestamp)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                """
                    cursor.execute(insert_query,
                                   (row['id_str'], row['name'], row['screen_name'], row['location'], row['url'],
                                    row['description'], row['verified'], row['followers_count'], row['friends_count'],
                                    row['listed_count'], row['favourites_count'], row['statuses_count'],
                                    row['created_at'],
                                    data['timestamp_ms']))
                    # cursor.commit()

                # If id already exists and the new timestamp is greater, update the row
                elif data['timestamp_ms'] > result[1]:
                    update_query = """
                                    UPDATE user SET id_str=%s, name=%s, screen_name=%s, location=%s, url=%s, description=%s, 
                                    verified=%s, followers_count=%s, friends_count=%s, listed_count=%s, favourites_count=%s, 
                                    statuses_count=%s, created_at=%s, timestamp=%s
                                    WHERE id_str=%s
                                    """
                    cursor.execute(update_query,
                                   (row['id_str'], row['name'], row['screen_name'], row['location'], row['url'],
                                    row['description'], row['verified'], row['followers_count'], row['friends_count'],
                                    row['listed_count'], row['favourites_count'], row['statuses_count'],
                                    row['created_at'],
                                    data['timestamp_ms'], row['id_str']))
                    # conn.commit()
            if 'quoted_status' in data.keys():
                row = data['quoted_status']['user']
                # Define the SQL query to check if id already exists in the table
                check_query = f"""
                                            SELECT id_str, timestamp FROM user WHERE id_str={row['id_str']}
                                            """
                cursor.execute(check_query)
                result = cursor.fetchone()

                # If id doesn't exist, insert the row into the table
                if result is None:
                    insert_query = """
                                                INSERT INTO user (id_str, name, screen_name, location, url, description, verified, followers_count,
                                                                 friends_count, listed_count, favourites_count, statuses_count, created_at, timestamp)
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                                """
                    cursor.execute(insert_query,
                                   (row['id_str'], row['name'], row['screen_name'], row['location'], row['url'],
                                    row['description'], row['verified'], row['followers_count'], row['friends_count'],
                                    row['listed_count'], row['favourites_count'], row['statuses_count'],
                                    row['created_at'],
                                    data['timestamp_ms']))
                    # cursor.commit()

                # If id already exists and the new timestamp is greater, update the row
                elif data['timestamp_ms'] > result[1]:
                    update_query = """
                                                    UPDATE user SET id_str=%s, name=%s, screen_name=%s, location=%s, url=%s, description=%s, 
                                                    verified=%s, followers_count=%s, friends_count=%s, listed_count=%s, favourites_count=%s, 
                                                    statuses_count=%s, created_at=%s, timestamp=%s
                                                    WHERE id_str=%s
                                                    """
                    cursor.execute(update_query,
                                   (row['id_str'], row['name'], row['screen_name'], row['location'], row['url'],
                                    row['description'], row['verified'], row['followers_count'], row['friends_count'],
                                    row['listed_count'], row['favourites_count'], row['statuses_count'],
                                    row['created_at'],
                                    data['timestamp_ms'], row['id_str']))
                    # conn.commit()
        except Exception as e:
            if line_ctr%2 != 0:
                print(line)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(exc_type, exc_tb.tb_lineno)
                break

#conn.commit()

line_ctr = 0
with open("corona-out-3", "r") as f1:
    for line in f1:
        line_ctr += 1
        try:
            row = json.loads(line)
            # check if the first two characters of the text column are "RT"
            if row['text'][0:2] == "RT" and 'retweeted_status' in row.keys():
                # check if the row already exists in the retweets table
                exists_query = "SELECT id_str FROM retweets WHERE id_str = %s"
                cursor.execute(exists_query, (row['id_str'],))
                exists = cursor.fetchone() is not None
                if not exists:
                    # insert the record into the retweets table
                    insert_query = "INSERT INTO retweets VALUES (%s, %s, %s, %s)"
                    values = (row['id_str'], row['retweeted_status']['id_str'],
                              row['user']['id_str'], row['user']['screen_name'])
                    cursor.execute(insert_query, values)
        except Exception as e:
            if line_ctr%2 != 0:
                print(line)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(exc_type, exc_tb.tb_lineno)
                break

# commit the changes and close the connection
conn.commit()
