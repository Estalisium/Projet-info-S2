import sqlite3

con = sqlite3.connect('Conditions_de_victoire.db')
cur = con.cursor()
print('Opened database successfully')

cur.execute("DROP TABLE Conditions_de_victoire")
cur.execute("""CREATE TABLE Conditions_de_victoire
            (nombre_j INT PRIMARY KEY NOT NULL,
             max_traque INT NOT NULL,
             max_secours INT NOT NULL)
             """)
con.commit()
cur.execute("""
    INSERT INTO Conditions_de_victoire VALUES
    (2, 7, 13),
    (3, 8, 14),
    (4, 9, 15),
    (5, 10, 16),
    (6, 11, 17),
    (7, 12, 18)
""")

con.commit()
res = cur.execute("SELECT * FROM Conditions_de_victoire")
print(res.fetchall())
print("Table created successfully")
cur.close()
