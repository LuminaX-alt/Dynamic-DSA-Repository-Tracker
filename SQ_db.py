# STEP 1: Setup SQLite DB
import sqlite3
import datetime

conn = sqlite3.connect('submissions.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    explanation TEXT,
    difficulty TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
