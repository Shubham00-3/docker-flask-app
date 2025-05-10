from flask import Flask
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="db",  # This matches our database service name in Docker Compose
        user="root",
        password="my-secret-pw",
        database="myapp"
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a table if it doesn't exist
    cursor.execute('CREATE TABLE IF NOT EXISTS visits (id INT AUTO_INCREMENT PRIMARY KEY, count INT)')
    # Increment visit count
    cursor.execute('INSERT INTO visits (count) VALUES (1) ON DUPLICATE KEY UPDATE count = count + 1')
    cursor.execute('SELECT count FROM visits LIMIT 1')
    count = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return f'<h1>Hello from my Docker App!</h1><p>Page visits: {count}</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
