import os
import sqlite3

db_filename = "gramguard.db"

# Close any lingering connections by recreating/overwriting tables
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Drop existing table to clear old schema
cursor.execute("DROP TABLE IF EXISTS complaints;")

# Recreate fresh table with ALL required columns
cursor.execute('''
    CREATE TABLE complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        village TEXT NOT NULL,
        category TEXT NOT NULL,
        complaint TEXT NOT NULL,
        priority TEXT NOT NULL,
        department TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        is_duplicate INTEGER DEFAULT 0,
        parent_id INTEGER DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()

print("✅ Database successfully reset with the new schema!")