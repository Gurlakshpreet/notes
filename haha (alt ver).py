from msilib.schema import ListBox
from re import I
import sqlite3
import time
import tkinter as tk
from tkinter import Frame, PhotoImage, Scrollbar, ttk
from time import strftime
import tkinter
from tkinter import font

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
bvar = "#70A9A1"
mochi = "#40798C"
sectbg = "#CFE0C3"
wind.config(bg = bvar)
defont = ('Bell Gothic Std Black', 10, 'bold')

def home():
    def onselect(a):
        o = titles.get(tkinter.ANCHOR)
        x = cur.execute("SELECT * FROM notebook WHERE page = ?", [(str(o))])
        a = []
        for i in x:
            a.append(i)
        h = bool(str(a[len(a) - 1])[3:-2])
        root.destroy()
        note(o, 1)
    def p():
        tip.grid(row = 0, column = 1, padx = 5, ipadx = 2)
        bb.config(text = "Back", command = btfo)
    def btfo():
        tip.grid_forget()
        bb.config(text = "Make Page", command = p)
    def time():
        t = strftime('%H:%M:%S')
        lbl.config(text = t)
        lbl.after(1000, time)
        seconds = str(round(((int(strftime('%H')) * 60 * 60 + int(strftime('%M')) * 60 + int(strftime('%S'))) / 86400) * 100)) + "%"
        perc.config(text = c(seconds, " of the day has passed"))
        perc.after(10000, time)
    def make():
        x = 0
        if titli.get() != "":
            for i in cur.execute("SELECT * FROM notebook WHERE page = ?", [(titli.get())]):
                x += 1
            if x != 0: 
                opl.config(text = "Page already exists")
            else:
                root.pack_forget()
                note(titli.get(), 0)
        else:
            opl.config(text = "Please enter a title: ")
    root = Frame(wind, bg = bvar, height = 450, width = 900)
    timms = Frame(root, bg = bvar)
    lbl = ttk.Label(timms, font = ('Bell Gothic Std Black', 60, 'bold'), foreground = "white", background = bvar)
    perc = ttk.Label(timms, font = ('Bell Gothic Std Black', 10, 'bold'), foreground = "white", background = bvar)
    timms.pack(padx = 15, pady = 15)
    time()
    lbl.pack()
    perc.pack()
    ti = Frame(root, bg = bvar)
    bb = tkinter.Button(ti, text = "Make Page", command = p, font=font.Font(family='Bell Gothic Std Black', size = 10), borderwidth = 0, bg = "white", fg = mochi)
    bb.grid(row = 0, column = 0)
    tip = Frame(ti, bg = sectbg)
    opl = ttk.Label(tip, text = "Title your page:", font = ('Bell Gothic Std Black', 10), foreground = 'white', background = sectbg)
    opl.grid(row = 0, column = 0)
    titli = tkinter.Entry(tip, width = 35, borderwidth = 0)
    titli.grid(row = 0, column = 1, pady = 5)
    openbtn = tkinter.Button(tip, text = "Make Page", command = make, font=font.Font(family='Bell Gothic Std Black', size = 10), borderwidth = 0, bg = "white", fg = sectbg)
    openbtn.grid(row = 0, column = 2, padx = 5, pady = 5)
    ti.pack()
    bed = Frame(root, background = sectbg, width = 700, height = 320)
    bed.pack(padx = 25, pady = 25)
    bed.pack_propagate(False)
    scroll = Scrollbar(bed, orient = tkinter.VERTICAL)
    titles = tkinter.Listbox(bed, yscrollcommand = scroll.set, borderwidth = 5, foreground = mochi, height = 300, width = 135, background = "white", relief = tkinter.FLAT, font = font.Font(family = 'Bell Gothic Std Black', size = 10))
    scroll.config(command = titles.yview)
    scroll.pack(side = tkinter.RIGHT, fill = tkinter.Y)
    titles.pack(padx = 4, pady = 4)
    cur.execute("SELECT * FROM notebook")
    if len(cur.fetchall()) != 0:
        p = []
        x = cur.execute("SELECT page FROM notebook")
        y = list(x.fetchall())
        for i in range(len(y)):
            if (y[i] not in p):
                p.append(y[i])
        for i in range(len(p)):
            x = str(p[i])[2:-3]
            titles.insert(tkinter.END, x)
            titles.bind('<<ListboxSelect>>', onselect)
    else:
        titles.pack_forget()
        scroll.pack_forget()
        tkinter.Label(bed, text = "Empty Notebook! Make a page?", foreground = "white", background = sectbg, font = ('Corbel', 10, 'bold'), width = 800).pack(pady = 25)
    root.pack(padx = 25, pady = 25)

def note(title, ver):
    def ext():
        ji.destroy()
        home()
    def save():
        y = 0
        x = cur.execute("SELECT * FROM notebook WHERE page = ?", [(title)])
        for i in x:
            y = 1
        if y == 1:
            cur.execute("DELETE FROM notebook WHERE page = ?", [(title)])
            x = cur.execute("SELECT * FROM notebook WHERE page = ?", [(title)])
            for i in x:
                y = 1
        cur.execute("INSERT INTO notebook (page, note) VALUES (?, ?)", (title, str(box.get(1.0, tkinter.END))))
        con.commit()
        x = cur.execute("SELECT * FROM notebook WHERE page = ?", [(title)])
        for i in x:
                y = 1
    ji = Frame(wind, height = 900, width = 900, bg = bvar)
    ji.pack()
    ji.pack_propagate(False)
    ttk.Label(ji, text = title, font = ('Bell Gothic Std Black', 15, 'bold'), background = bvar, foreground = sectbg).pack(pady = (13, 0))
    col = Frame(ji, width = 900, height = 450, background = sectbg)
    boxy = Frame(col, width = 800, height = 350, background = sectbg)
    col.pack(padx = 50, pady = (0, 25))
    col.pack_propagate(False)
    boxy.pack()
    boxy.pack_propagate(False)
    box = tkinter.Text(boxy, width = 800, wrap = tkinter.WORD, borderwidth = 0)
    box.pack()
    innit = Frame(col, background = sectbg)
    tkinter.Button(innit, text = "Save", command = save, font = font.Font(family='Bell Gothic Std Black', size = 10), borderwidth = 0, bg = "white", fg = mochi).grid(row = 0, column= 0, padx = (7, 0))
    tkinter.Button(innit, text = "Exit", command = ext, borderwidth = 0, font = font.Font(family='Bell Gothic Std Black', size = 10), fg = sectbg, bg = bvar).grid(row = 0, column = 1, padx = (7.5, 15))
    innit.pack(pady = 5)
    boxy.pack()
    if ver == 1:
        for i in cur.execute("SELECT * FROM notebook WHERE page = ?", [(title)]):
            o = 6 + int(len(title))
            x = str(i).replace(r'\n', '\n')[o : -2]
        box.insert(tkinter.INSERT, x)

home()

wind.mainloop()
