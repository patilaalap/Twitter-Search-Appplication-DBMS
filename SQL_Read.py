import pymysql

# Making a class for MySQL database
class UserDatabase:
    def __init__(self):
        self.conn = pymysql.connect(user='root',
                              password='#Aalap21',
                              host='localhost',
                              database = 'user_db',
                              )
        self.cursor = self.conn.cursor()

# Query to select username and screen_name according to the searched username
    def get_user_by_name(self, username,offset):
        #sql = f"SELECT * FROM user WHERE name='{username}'"
        sql = f"SELECT name,screen_name FROM user WHERE screen_name LIKE '{username}%' ORDER BY followers_count DESC LIMIT 10 OFFSET {offset}"
        self.cursor.execute(sql)
        #self.cursor.execute("SELECT * FROM user WHERE id_str = '804046791348015107'")
        result = self.cursor.fetchall()
        return self.get_userdetails_list(result)

# Query to select user details according to the searched username
    def get_userdetails(self,Uname):
        sql = f"SELECT name, screen_name,location,description,followers_count,friends_count,created_at from user WHERE screen_name = '{Uname}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return self.get_userdetails_list(result)

# Query to get the top 10 users according to the followers
    def get_top_ten(self):
        sql = f"SELECT name, screen_name from user ORDER BY followers_count DESC LIMIT 10"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return self.get_userdetails_list(result)

# Query to get the users who retweeted according to the tweet ID
    def retweets(self, original_tweet_id):
        sql = f"SELECT screen_name from retweets WHERE original_tweet_id = '{original_tweet_id}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return self.get_userdetails_list(result)

# To retrieve all details as a list for cache
    def get_userdetails_list(self, result):
        L= []
        for detail in result:
            L.append(detail)
        return L
