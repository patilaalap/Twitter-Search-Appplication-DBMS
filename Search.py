from SQL_Read import UserDatabase
#import ipywidgets as widgets

import tkinter as tk
#from IPython.display import display, clear_output
#import sqlite3
import re

#username = input("Enter the username: ")


def clear_frame():
    for widgets in frame.winfo_children():
        widgets.destroy()


def retrieve_input():
    x = e1.get()
    pattern = r"^@"
    pattern_hashtag = r"^#"
    if re.match(pattern,x):
        user_obj = UserDatabase()
        y = user_obj.get_user_by_name(x[1:])
        i = 0
        for rows in y:
            uname = rows[1]
            link = tk.Label(frame, text=rows[1], font=('Helveticabold', 15), fg="blue", cursor="hand2")
            link.grid(row=i + 3, column = 0)
            link.bind("<Button-1>", lambda event: user_details(event, uname))
            link = tk.Label(frame, text=rows[0], font=('Helveticabold', 15))
            link.grid(row=i + 3, column=1)
            i = i+1
        tk.mainloop()
    elif re.match(pattern_hashtag,x):
        print("# pattern")
    else:
        print("Text")

def user_details(event, uname):
    clicked_label = event.widget
    label_text = clicked_label.cget("text")
    clear_frame()
    user_obj = UserDatabase()
    user_det = user_obj.get_userdetails(label_text)
    for rows in user_det:
        tk.Label(frame, text=rows).grid(row=2)
    tk.mainloop()

master = tk.Tk()
master.title('Twitter search application')
master.geometry("600x350")
frame = tk.Frame(master, height=1, width=10)
frame.pack()
tk.Label(frame, text='Search').grid(row=0)
e1 = tk.Entry(frame)
e1.grid(row=1)

buttonCommit = tk.Button(frame, height=1, width=10, text="Search", command=lambda: retrieve_input())
buttonCommit.grid(row=2)
tk.mainloop()