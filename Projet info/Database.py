import sqlite3

con = sqlite3.connect('cartes.db')
cur = con.cursor()
print('Opened database successfully')

cur.execute("DROP TABLE survie")
cur.execute("""CREATE TABLE survie
            (c_id INT PRIMARY KEY NOT NULL,
             nom VARCHAR2(30) NOT NULL,
             e_id INT NOT NULL)""")
con.commit()
cur.execute("""
    INSERT INTO survie VALUES
        (1, 'test', 1),
        (2, 'test2', 2)
""")
con.commit()
res = cur.execute("SELECT * FROM survie")
print(res.fetchall())
print("Table created successfully")
cur.close()