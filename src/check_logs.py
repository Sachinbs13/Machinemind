import sqlite3

conn = sqlite3.connect("../data/machinemind.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM sensor_data")
print("sensor_data:", cursor.fetchall())

cursor.execute("SELECT * FROM maintenance_records")
print("maintenance_records:", cursor.fetchall())

conn.close()