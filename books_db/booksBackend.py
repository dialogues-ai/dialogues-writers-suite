import sqlite3
import json

def connect():
    conn = sqlite3.connect("dialoguebooks.db")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys=ON;")
    cur.execute("CREATE TABLE IF NOT EXISTS book (bookid INTEGER PRIMARY KEY, "
                + "gutenberg INTEGER, title text, genre text, author text)")
    cur.execute("CREATE TABLE IF NOT EXISTS emoarc (bookid INTEGER, "
                + "points BLOB, FOREIGN KEY(bookid) REFERENCES book(bookid))")
    conn.commit()
    conn.close()

def insert(gutenberg, title, genre, author, emoarc=None):
    conn = sqlite3.connect("dialoguebooks.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO book VALUES (NULL,?,?,?,?)",
                (gutenberg, title, genre, author))
    if type(emoarc) == list:
        cur.execute("SELECT bookid FROM book WHERE gutenberg=? AND title=? "
                        + "AND genre=? AND author=?",
                        (gutenberg, title, genre, author))
        rows = cur.fetchall()
        if len(rows) != 1:
            print("ERROR: couldn't get inserted row; emoarc not inserted",
                      len(row), row)
        cur.execute("INSERT INTO emoarc VALUES (?,?)",
                        (rows[0][0], json.dumps(emoarc)))
    conn.commit()
    conn.close()
    
def view():
    conn = sqlite3.connect("dialoguebooks.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(gutenberg="", title="", genre="", author=""):
    conn = sqlite3.connect("dialoguebooks.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book WHERE gutenberg=? OR title=? OR genre=? OR author=?", (gutenberg, title, genre, author))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("dialoguebooks.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
def update(id, gutenberg, title, genre, author):
    conn = sqlite3.connect("dialoguebooks.db")
    cur = conn.cursor()
    cur.execute("UPDATE book SET gutenberg=?, title=?, genre=?, author=? WHERE id=?", (gutenberg, title, genre, author))
    conn.commit()
    conn.close()

connect()

