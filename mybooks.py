# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 03:57:44 2021

@author: Asus
"""
from tkinter import Tk, Button, Label,Scrollbar,Listbox,StringVar,Entry,W,E,N,S,END
from tkinter import ttk
from tkinter import messagebox
from mysql_config import dbConfig
import mysql.connector as pyo

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
    list_bx.delete(0, 'end')
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
        

    