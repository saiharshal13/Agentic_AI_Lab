import sqlite3

def run_sql(query):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()


if __name__ == "__main__":
    print(run_sql("SELECT * FROM students"))