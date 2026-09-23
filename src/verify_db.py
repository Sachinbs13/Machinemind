import sqlite3

conn = sqlite3.connect("../data/machinemind.db")
cursor = conn.cursor()

cursor.execute("INSERT OR IGNORE INTO machines (machine_id, type) VALUES (?, ?)", ("M001", "M"))
conn.commit()

cursor.execute("SELECT * FROM machines")
print(cursor.fetchall())

conn.close()