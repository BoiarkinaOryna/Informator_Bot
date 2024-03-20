import sqlite3

connect = None
cursor = None
open_db = True

def create_table(name_table: str):
    global connect, cursor, open_db
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    open_db = True
    print("Create table")
    if name_table == "Administartors":
        cursor.execute("CREATE TABLE IF NOT EXISTS Administrators (email TEXT, nickname TEXT, password TEXT, phone_number TEXT)")
    if name_table == "Clients":
        cursor.execute("CREATE TABLE IF NOT EXISTS Clients (id TEXT, email TEXT, nickname TEXT, phone_number TEXT)")
    connect.commit()

def write_data(table: str, my_email: str, my_nick: str, my_number: str, id = None, my_password = None):
# def write_data(column1: str, table: str, data1: str, column2: str, data2: str):
    global cursor, connect, open_db
    if open_db == False:
        connect = sqlite3.connect("database.db")
        cursor = connect.cursor()
        open_db = True
    
    # write_data = f"INSERT INTO {table} ({column}) VALUES ({data})"
    if table == "Administrators":
        create_table(name_table = "Administartors")
        write_data = f"INSERT INTO {table} (email, nickname, password, phone_number) VALUES ('{my_email}', '{my_nick}', '{my_password}', '{my_number}')"
    if table == "Clients":
        create_table(name_table = "Clients")
        write_data = f"INSERT INTO {table} (id, email, nickname, phone_number) VALUES ('{id}', '{my_email}', '{my_nick}', '{my_number}')"
        print("insert into")
    cursor.execute(write_data)
    connect.commit()
    connect.close()
    open_db = False