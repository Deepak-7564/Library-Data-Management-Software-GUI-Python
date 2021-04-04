# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 02:31:02 2021

@author: Asus
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 01:34:14 2021

@author: Asus
"""
from tkinter import Tk, Button,Label,Scrollbar,Listbox,StringVar,Entry,W,E,N,S,END
from tkinter import ttk
from tkinter import messagebox
from mysql_config import dbConfig
import mysql.connector as pyo


root = Tk()

#connector

con =pyo.connect(**dbConfig)

cursor = con.cursor()

class Bookdb:
    def __init__(self):
        self.con = pyo.connect(**dbConfig)
        self.cursor = con.cursor()
        print("You have connected to the database")
        print(con)
        
    def __del__(self):
        self.con.close()
        
    def view(self):
        self.cursor.exwcute("SELECT * FROM books")
        rows =self.cursor.fetchall()
        return rows
    
    def insert(self,title,author,isbn):
        sql =("INSERT INTO books(title,author,isbn)VALUES (%s,%s,%s)")
        values =[title,author,isbn]
        self.cursor.execute(sql,values)
        self.con.commit()
        messagebox.showinfo(title="Book Database",message="New book added to database")
        
    def update(self, id, title, author, isbn):
        tsql ='UPDATE books SET title = %s, author = %s, isbn =%s WHERE id=%s'
        self.cursor.execute(tsql,[title,author,isbn,id])
        self.con.commit()
        messagebox.showinfo(title="Book Database",message="Book updated")
        
    def delete(self,id):
        delquery = 'DELETE FROM books WHERE id = %s'
        self.cursor.execute(delquery, [id])
        self.con.commit()
        messagebox.showinfo(title="Book Database",message="Book Deleted")
        
db = Bookdb()

def get_selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)
    title_entry.delete(0,'end')
    title_entry.insert('end', selected_tuple[1])
    author_entry.delete(0, 'end')
    author_entry.insert('end', selected_tuple[2])
    isbn_entry.delete(0, 'end')
    isbn_entry.insert('end',selected_tuple[3])
    
def view_records():
    list_dx.delete(0, 'end')
    for row in db.view():
        list_bx.insert('end', row)
    
def add_book():
    db.insert(title_text.get(),author_text.get(),isbn_text.get())
    list_dx.delete(0,'end')
    list_bx.insert('end',(title_text.get(),author_text.get(), isbn_text.get()))
    title_entry.delete(0,"end")
    author_entry.delete(0,"end")
    isbn_entry.delete(0,"end")
    con.commit()
    
def delete_records():
    db.delete(selected_tuple[0])
    con.commit()
    
def clear_screen():
    list_bx.delete(0,'end')
    title_entry.delete(0,'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0 , 'end')
    
def update_records():
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
    title_entry.delete(0, "end")
    author_entry.delete(0,"end")
    isbn_entry.delete(0,"end")
    con.commit()
    
def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        del dd



#GUI

root.title("Library Database App")
root.configure(background="light green")
root.geometry("850x500")
root.resizable(width=False,height=False)

title_label = ttk.Label(root,text="Title",background="light blue",font=("TkDefaultFont", 16))
title_label.grid(row=0,column=0, sticky=W,padx=5)
title_text= StringVar()
title_entry = ttk.Entry(root,width=24,textvariable=title_text)
title_entry.grid(row=0, column=1, sticky =W)

author_label = ttk.Label(root,text="Author",background="light blue",font=("TkDefaultFont", 16))
author_label.grid(row=0,column=2, sticky=W,padx=5)
author_text= StringVar()
author_entry = ttk.Entry(root,width=24,textvariable=author_text)
author_entry.grid(row=0, column=3, sticky =W)

isbn_label = ttk.Label(root,text="ISBN",background="light blue",font=("TkDefaultFont", 16))
isbn_label.grid(row=0,column=4, sticky=W)
isbn_text= StringVar()
isbn_entry = ttk.Entry(root,width=24,textvariable=isbn_text)
isbn_entry.grid(row=0, column=5, sticky =W)

add_btn = Button(root, text="Add Book",bg="blue",fg="white",font="helevetica 10 bold",command = add_book)
add_btn.grid(row=0,column=6,sticky=W,padx=20)


# Middle Part 
list_bx = Listbox(root,height=16,width=40, font = "helvetica 13",bg ="light blue")
list_bx.grid(row=3,column=1, columnspan=14,sticky=W +E,pady=40,padx=15)
list_bx.bind('<<ListboxSelect>>',get_selected_row)


scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1,column=8, rowspan =14,sticky =W)

list_bx.configure(yscrollcommand =scroll_bar.set)
scroll_bar.configure(command=list_bx.yview)


#Lower Buttons

delete_btn = Button(root, text="Delete Record",bg="purple",fg="white",font="helvetica 10 bold",command=delete_records)
delete_btn.grid(row=15,column=1)

clear_btn = Button(root, text="Cear Screen",bg="purple",fg="white",font="helvetica 10 bold",command=clear_screen)
clear_btn.grid(row=15,column=2)

exit_btn = Button(root, text="EXIT Application",bg="purple",fg="white",font="helvetica 10 bold",command=root.destroy)
exit_btn.grid(row=15,column=3)

modify_btn = Button(root, text="Modify Record",bg="purple",fg="white",font="helvetica 10 bold",command=update_records)
modify_btn.grid(row=15,column=4)

view_btn = Button(root, text="View all records",bg="purple",fg="white",font="helvetica 10 bold",command=view_records)
view_btn.grid(row=15,column=5)




#Main Loop

root.mainloop()
