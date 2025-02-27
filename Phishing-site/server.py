from flask import Flask, render_template, request, jsonify, url_for
import sqlite3
import logging

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verification')
def verification():
    return render_template('verification.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            logging.warning("Invalid JSON received")
            return jsonify({'error': 'Invalid JSON'}), 400
        username = data['username']
        password = data['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('BEGIN TRANSACTION') # Додаємо транзакцію
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        logging.info(f"User {username} logged in successfully")
        return jsonify({'redirect': '/verification'})
    except Exception as e:
        conn.rollback() # Відкочуємо транзакцію у разі помилки
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': f'An error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)