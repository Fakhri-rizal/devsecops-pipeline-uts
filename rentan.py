import sqlite3

def login(username, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # RENTAN SQL INJECTION: input user digabung langsung tanpa parameterized query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"Menjalankan query: {query}")
    
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

if __name__ == "__main__":
    user_input = input("Masukkan username: ")
    pass_input = input("Masukkan password: ")
    login(user_input, pass_input)