#import sqlite3
import pymysql

class UserDatabase:
    def __init__(self):
        self.conn = pymysql.connect(user='root',
                              password='RushabhK',
                              host='localhost',
                              database = 'user_db',
                              )
        self.cursor = self.conn.cursor()


    def get_user_by_name(self, username,offset):
        #sql = f"SELECT * FROM user WHERE name='{username}'"
        sql = f"SELECT name,screen_name FROM user WHERE screen_name LIKE '{username}%' ORDER BY followers_count DESC LIMIT 10 OFFSET {offset}"
        self.cursor.execute(sql)
        #self.cursor.execute("SELECT * FROM user WHERE id_str = '804046791348015107'")
        result = self.cursor.fetchall()
        return result

    def get_userdetails(self,Uname):
        sql = f"SELECT name, screen_name,location,description,followers_count,friends_count,created_at from user WHERE screen_name = '{Uname}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def get_top_ten(self,Uname):
        sql = f"SELECT name, screen_name from user ORDER BY followers_count DESC LIMIT 10'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result