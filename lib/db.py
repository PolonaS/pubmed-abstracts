import sqlite3

conn = None


def create_connection():
    return sqlite3.connect('db.sqlite')


def create_table():
    global conn

    sql = """
        CREATE TABLE IF NOT EXISTS 
        acronyms(id integer PRIMARY KEY AUTOINCREMENT, article_id integer, acronym text, definition text)
    """

    try:
        if conn is None:
            conn = create_connection()
        c = conn.cursor()
        c.execute(sql)
        c.execute("DELETE FROM acronyms")
        conn.commit()
        c.close()
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)


def insert(id, acronym, definition):
    global conn

    sql = """
        INSERT INTO acronyms(article_id, acronym, definition)
        VALUES(?, ?, ?)
    """

    try:
        if conn is None:
            conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql, [id, acronym, definition])
        conn.commit()
        cur.close()
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)
