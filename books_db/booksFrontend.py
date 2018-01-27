from tkinter import *
import booksBackend

'''
Author: Alexander Yukhananov
Contributor(s): Jonny Johnson, Chrisil
Organization: Dialogues.ai 
Version: 0.1

To make an executable or application of this code, build 
the distribution using pyinstaller. 

From the terminal:
pyinstaller booksFrontend.py
OR 
pyinstaller --onefile --windowed booksFrontend.py
'''

def get_selected_row(event):
    try:
        global selected_tuple
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0,END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0,END)
        e2.insert(END,selected_tuple[2])
        e3.delete(0,END)
        e3.insert(END, selected_tuple[3])
        e4.delete(0,END)
        e4.insert(END, selected_tuple[4])
    except IndexError:
        pass

def view_command():
    list1.delete(0, END)
    for row in booksBackend.view():
        list1.insert(END, row)
        
def search_command():
    list1.delete(0, END)
    for row in booksBackend.search(gutenberg_text.get(), title_text.get(), genre_text.get(), author_text.get()):
        list1.insert(END, row)
        
def add_command():
    booksBackend.insert(gutenberg_text.get(), title_text.get(), genre_text.get(), author_text.get())
    list1.delete(0, END)
    list1.insert(END,(gutenberg_text.get(), title_text.get(), genre_text.get(), author_text.get()))

def delete_command():
    booksBackend.delete(selected_tuple[0])
    
def update_command():
    booksBackend.update(selected_tuple[0],gutenberg_text.get(), title_text.get(), genre_text.get(), author_text.get())
    
window=Tk()

window.wm_title("Dialogues Database")

l1 = Label(window, text = "Gutenberg Id")
l1.grid(row = 0, column = 0)
gutenberg_text = StringVar()
e1 = Entry(window, textvariable=gutenberg_text)
e1.grid(row=0, column = 1)


l2 = Label(window, text = "Title")
l2.grid(row = 0, column = 2)
title_text = StringVar()
e2 = Entry(window, textvariable=title_text)
e2.grid(row=0, column = 3)

l3 = Label(window, text = "Genre")
l3.grid(row = 1, column = 0)
genre_text = StringVar()
e3 = Entry(window, textvariable=genre_text)
e3.grid(row=1, column = 1)

l4 = Label(window, text = "Author")
l4.grid(row = 1, column = 2)
author_text = StringVar()
e4 = Entry(window, textvariable=author_text)
e4.grid(row=1, column = 3)

list1 = Listbox(window, height = 6, width = 35)
list1.grid(row = 2, column = 0, rowspan = 6, columnspan = 2)

sb1=Scrollbar(window)
sb1.grid(row = 2, column = 2, rowspan = 6)
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)


b1 = Button(window, text= "View all", width = 12, command=view_command)
b1.grid(row=2, column = 3)

b2 = Button(window, text= "Search entry", width = 12, command=search_command)
b2.grid(row=3, column = 3)

b3 = Button(window, text= "Add entry", width = 12, command=add_command)
b3.grid(row=4, column = 3)

b4 = Button(window, text= "Update selected", width = 12, command=update_command)
b4.grid(row=5, column = 3)

b5 = Button(window, text= "Delete selected", width = 12, command=delete_command)
b5.grid(row=6, column = 3)

b6 = Button(window, text= "Close", width = 12, command=window.destroy)
b6.grid(row=7, column = 3)


window.mainloop()