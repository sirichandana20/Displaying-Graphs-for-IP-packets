import sqlite3


conn = sqlite3.connect('database.db')

#conn.execute('CREATE TABLE Users (rowid INTEGER PRIMARY KEY AUTOINCREMENT,role varchar(30), name varchar(50), email varchar(50) UNIQUE, pwd varchar(12))')
#conn.execute("INSERT INTO Users (role, name, email, pwd) VALUES ('admin','chandana','chandana@gmail.com', '1')")

#conn.execute("Drop table Users")



res = conn.execute("SELECT * from Users")
for row in res:
    print(row)


'''
try:
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO Users (name, email, pwd) VALUES ('chandana', 'sirifeb20@yahoo.com', '1234')")
        con.commit()
        msg = "User Registered, Please login"
        print(msg)
except:
    con.rollback()
    print(con)
    msg = "error in insertion of the operation"
finally:
    con.close()
'''
