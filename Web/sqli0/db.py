import sqlite3

def create_table():
    db = sqlite3.connect("./sqli.db")
    cursor = db.cursor()
    try:
        cursor.execute('''CREATE TABLE user (username text,password text )''')
    except:
        pass
    return None

def create_admin():
    db = sqlite3.connect("./sqli.db")
    cursor = db.cursor()
    cursor.execute("insert into user values('admin', 'sPMoodmH0CNMHhsxnsGv')")
    db.commit()
    return None

create_table()
create_admin()
