from flask import Flask, request, send_from_directory, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

# MySQL connection config - adjust as needed
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Set your MySQL password
    'database': 'music_school'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def create_table_if_not_exists():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        return 'All fields are required', 400

    try:
        create_table_if_not_exists()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)', (name, email, message))
        conn.commit()
        cursor.close()
        conn.close()
        return 'Thank you for your message! We will get back to you soon.'
    except mysql.connector.Error as err:
        return f'Database error: {err}', 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)