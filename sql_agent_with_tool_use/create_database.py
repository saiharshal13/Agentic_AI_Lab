import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    year INTEGER
)
""")

students = [
    (1, "Koushik", "Cyber Security", 4),
    (2, "Jashwanth", "CSE", 3),
    (3, "Shiva", "Cyber Security", 4),
    (4, "Sneha", "AIML", 3),
    (5, "Vivek", "Cyber Security", 2),
    (6, "Dharma", "CSE", 4),
    (7, "Ravi", "AIML", 2)
]

cursor.executemany(
    "INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?)",
    students
)

conn.commit()
conn.close()

print("Database created successfully!")