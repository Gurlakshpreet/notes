from msilib.schema import ListBox
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
sectbg = "#653818"
bvar = "#f5cd95"
mochi = "#858861"
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
        note(o, h, 1)
    def p():
        root.pack_forget()
        title()
    def time():
        t = strftime('%H:%M:%S')
        lbl.config(text = t)
        lbl.after(1000, time)
        seconds = str(round(((int(strftime('%H')) * 60 * 60 + int(strftime('%M')) * 60 + int(strftime('%S'))) / 86400) * 100)) + "%"
        perc.config(text = c(seconds, " of the day has passed"))
        perc.after(10000, time)
    root = Frame(wind, bg = bvar, height = 450, width = 900)
    timms = Frame(root, bg = bvar)
    lbl = ttk.Label(timms, font = ('Bell Gothic Std Black', 60, 'bold'), foreground = "white", background = bvar)
    perc = ttk.Label(timms, font = ('Bell Gothic Std Black', 10, 'bold'), foreground = "white", background = bvar)
    timms.pack(padx = 15, pady = 15)
    time()
    lbl.pack()
    perc.pack()
    tkinter.Button(root, text = "Make Page", command = p, font=font.Font(family='Bell Gothic Std Black', size = 10), borderwidth = 0, bg = "white", fg = mochi).pack()
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

def title():
    def timothee():
        if timmy['text'] == "YES":
            timmy.config(text = "NO")
            cheeze.config(text = "Your page will not store time")
        else:
            timmy.config(text = "YES")
            cheeze.config(text = "Your page will store time")
    def create():
        x = 0
        if titli.get() != "":
            for i in cur.execute("SELECT * FROM notebook WHERE page = ?", [(titli.get())]):
                x += 1
            if x > 0: 
                additional.pack()
            else: 
                title = titli.get()
                t = True if timmy['text'] == "YES" else False
                scree.pack_forget()
                note(title, t, 0)
        else:
            cheeze.config(text = "Please enter a title", foreground = sectbg)
    def uwu():
        additional.pack_forget()
        titli.delete(0, tkinter.END)
    def lead():
        scree.pack_forget()
        t = True if timmy['text'] == "YES" else False
        note(titli.get(), t, 1)
    scree = Frame(wind, bg = bvar)
    scree.pack(fill = "both", expand = True, pady = 90)
    ti = Frame(scree, background = bvar)
    ttk.Label(ti, text = "Title your page:", font = ('Bell Gothic Std Black', 10), foreground = 'white', background = bvar).grid(row = 0, column = 0)
    titli = tkinter.Entry(ti, width = 35, borderwidth = 0)
    ti.pack(pady = 5)
    titli.grid(row = 0, column= 1)
    tim = Frame(scree, background = bvar)
    ttk.Label(tim, text = "Store time? (Click to change):", font = ('Bell Gothic Std Black', 10), foreground = 'white', background = bvar).grid(row = 0, column = 0)
    timmy = tkinter.Button(tim, text = "YES", command = timothee, font = font.Font(family='Bell Gothic Std Black', size = 10), borderwidth = 0, bg = "white", fg = mochi)
    cheeze = ttk.Label(scree, text = "Your page will store time", font = ('Bell Gothic Std Black', 10), foreground = 'white', background = bvar)
    tim.pack(pady = 5)
    timmy.grid(row = 0, column = 2)
    cheeze.pack(pady = 5)
    tkinter.Button(scree, text = "Create Page", command = create, font=font.Font(family='Bell Gothic Std Black', size = 10), borderwidth = 0, bg = sectbg, fg = "white").pack(pady = 5)
    additional = Frame(scree, bg = bvar)
    msg = ttk.Label(additional, background = bvar, foreground = sectbg, text = "This page already exists, open existing page or pick a new title?")
    btnlist = Frame(additional, bg = bvar)
    msg.pack()
    tkinter.Button(btnlist, text = "Open Existing Page", bg = sectbg, fg = "white", borderwidth = 0, command = lead).grid(row = 0, column = 0)
    spac = Frame(btnlist, bg = bvar, width = 1, background = bvar)
    spac.grid(row = 0, column = 1, padx = 10)
    tkinter.Button(btnlist, text = "Pick a New Title", bg = sectbg, fg = "white", borderwidth = 0, command = uwu).grid(row = 0, column = 2)
    btnlist.pack(padx = 10, pady = 10)

def note(title, timmy, func):
    h = []
    w = []
    def note():
        haha = input.get() if timmy == False else c(str(time.ctime()), ": ", input.get())
        h.append(haha)
        list.insert(tkinter.END, str(haha))
        input.delete(0, tkinter.END)
    def save():
        con.commit()
        for i in range(len(h)):
            h.append(timmy)
            cur.execute("INSERT INTO notebook (page, note) VALUES (?, ?)", (title, h[i]))
            con.commit()
        h.clear()
    def ext():
        screen.destroy()
        home()
    def write():
        x = cur.execute("SELECT * FROM notebook WHERE page = ?", [(str(title))])
        for i in x:
            i = str(i)
            o = int(len(title) + 6)
            i = i[o : -2]
            w.append(i)
        t = w[len(w) - 1]
        for i in range(len(w)):
            list.insert(tkinter.END, str(w[i]))
    wind.config(bg = bvar)
    screen = Frame(wind, bg = bvar)
    screen.pack(fill = "both", expand = True, pady = 50)
    bg = Frame(screen, height = 350, width = 800, bg = mochi)
    bg.pack()
    header = Frame(bg, bg = mochi)
    ttk.Label(header, text = title, font = ('Bell Gothic Std Black', 15, 'bold'), background = mochi, foreground = sectbg).pack(padx = 5) 
    header.pack()
    nf = Frame(bg, width = 800, bg = mochi, height = 270)
    nf.pack_propagate(False)
    nf.pack()
    nfscroll = Scrollbar(nf, orient = tkinter.VERTICAL)
    sfscroll = Scrollbar(nf, orient = tkinter.HORIZONTAL)
    list = tkinter.Listbox(nf, yscrollcommand = nfscroll.set, xscrollcommand = sfscroll.set, borderwidth = 0, background = mochi, height = 280, width = 770, foreground = "white", selectbackground = "white", selectforeground = mochi)
    nfscroll.config(command = list.yview)
    sfscroll.config(command = list.xview)
    nfscroll.pack(side = tkinter.RIGHT, fill = tkinter.Y)
    sfscroll.pack(side = tkinter.BOTTOM, fill = tkinter.X)
    list.pack(padx = 25, pady = (0, 40))
    bg.pack_propagate(False)
    inp = Frame(bg, height = 50, width = 1000, bg = sectbg)
    inp.place(x = 0, y = 300)
    space = Frame(inp, bg = sectbg, height = 30)
    space2 = Frame(inp, bg = sectbg, height = 30)
    ttk.Label(inp, text = "Make note:", font = ('Bell Gothic Std Black', 10), foreground = 'white', background = sectbg).grid(row = 0, column = 0, padx = (10, 0))
    input = tkinter.Entry(inp, width = 91, borderwidth = 0)
    input.grid(row = 0, column = 1, padx = (5, 10))
    tkinter.Button(inp, text = "Save", command = save, font=font.Font(family='Bell Gothic Std Black', size = 10), borderwidth = 0, bg = "white", fg = mochi).grid(row = 0, column = 4)
    space.grid(row = 0, column = 3, padx = (5, 10), pady = 10)
    space2.grid(row = 0, column = 5, padx = 3, pady = 10)
    tkinter.Button(inp, text = "Enter", command = note, font = font.Font(family='Bell Gothic Std Black', size = 10), borderwidth = 0, bg = "white", fg = mochi).grid(row = 0, column= 2, padx = (7, 0))
    tkinter.Button(inp, text = "Exit", command = ext, borderwidth = 0, font = font.Font(family='Bell Gothic Std Black', size = 10), fg = sectbg, bg = bvar).grid(row = 0, column = 6, padx = (7.5, 15))
    if func == 1:
        write()

home()

wind.mainloop()