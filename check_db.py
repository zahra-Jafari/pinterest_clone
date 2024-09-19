import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(images_image);")
print(cursor.fetchall())

conn.close()
