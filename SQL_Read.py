import sqlite3

class UserDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('user_db.db')
        self.cursor = self.conn.cursor()

    def get_user_by_name(self, username,offset):
        #sql = f"SELECT * FROM user WHERE name='{username}'"
        sql = f"SELECT name,screen_name FROM user WHERE screen_name LIKE '{username}%' ORDER BY followers_count DESC LIMIT 10 OFFSET '{offset}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def get_userdetails(self,Uname):
        sql = f"SELECT name, screen_name,location,description,followers_count,friends_count,created_at from user WHERE screen_name = '{Uname}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
