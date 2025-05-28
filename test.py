import sqlite3

def test_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users")
    rows = cursor.fetchall()

    if not rows:
        print("No users found.")
    else:
        print("Registered users:")
        for row in rows:
            print(f"ID: {row[0]}, Username: {row[1]}, Email: {row[2]}")

    conn.close()

if __name__ == '__main__':
    test_users()
