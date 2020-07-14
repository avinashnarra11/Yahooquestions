import sqlite3
import os.path

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#db_path = os.path.join(BASE_DIR, "yahoo_new.db")
#print(db_path)
conn = sqlite3.connect("../../yahoo_new.db")

cur = conn.cursor()

cur.execute("SELECT * FROM questions_tb")
# rows = cur.fetchall()
# for row in rows:
#     print(row)

conn.commit()
