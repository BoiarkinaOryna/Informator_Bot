import sqlite3

def get_all_id():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT id FROM Clients")
    select_id = cursor.fetchall()
    db.close()
    return select_id