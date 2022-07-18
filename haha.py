from msilib.schema import ListBox
import sqlite3
import time
import tkinter as tk
from tkinter import Frame, PhotoImage, Scrollbar, ttk
from time import strftime
import tkinter
from tkinter import font
from typing import Text

con = sqlite3.connect("mess.db")
cur = con.cursor()
cur.execute("CREATE TABLE if not exists notebook (page VARCHAR, note VARCHAR)")
con.commit()

def c(*s):
    w = ""
    for i in range(len(s)):
        w = w + str(s[i])
    return w

wind = tk.Tk()
wind.resizable(False,False)
wind.title("Notes")
wind.geometry('900x450')
sectbg = "#653818"
bvar = "#f5cd95"
mochi = "#858861"
wind.config(bg = bvar)
defont = ('Bell Gothic Std Black', 10, 'bold')

def y():
    Tik.delete(1.0, tkinter.END)
    Tik.insert(tkinter.INSERT, T.get(1.0, tkinter.END))
    print(T.get(1.0, tkinter.END))

T = tkinter.Text(wind, height = 5, width = 52, wrap = tkinter.WORD)

b = tkinter.Button(wind, text = ".", command = y)

Tik = tkinter.Text(wind, height = 5, width = 52, wrap = tkinter.WORD)

T.pack()
b.pack()
Tik.pack()

wind.mainloop()