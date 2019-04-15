import sqlite3

conn = None


def create_connection():
    return sqlite3.connect('db.sqlite')


def create_table():
    global conn
    if conn is None:
        conn = create_connection()
    c = conn.cursor()
    sql = """
        CREATE TABLE IF NOT EXISTS 
        acronyms(id integer PRIMARY KEY AUTOINCREMENT, article_id integer, acronym text, definition text)
    """
    c.execute(sql)
    c.execute("DELETE FROM acronyms")
    c.close()


def insert(id, acronym, definition):
    global conn
    if conn is None:
        conn = create_connection()
    sql = """
        INSERT INTO acronyms(article_id, acronym, definition)
        VALUES(?, ?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, [id, acronym, definition])
    cur.close()
