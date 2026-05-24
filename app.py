from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TABLES
def create_tables():
    conn = get_db_connection()

    # USERS TABLE
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # NOTES TABLE
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

create_tables()

# LOGIN PAGE
@app.route('/')
def login_page():
    return render_template('login.html')

# SIGNUP PAGE
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# NOTES PAGE
@app.route('/notes')
def notes_page():
    return render_template('index.html')

# REGISTER USER
@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()

    existing_user = conn.execute(
        'SELECT * FROM users WHERE username = ?',
        (username,)
    ).fetchone()

    if existing_user:
        conn.close()
        return jsonify({'message': 'User already exists'})

    conn.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, password)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Registration successful'})


# LOGIN USER
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()

    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()

    conn.close()

    if user:
        return jsonify({'success': True})

    return jsonify({'success': False})


# ADD NOTE
@app.route('/add_note', methods=['POST'])
def add_note():

    data = request.get_json()

    content = data.get('content')

    created_at = datetime.now().strftime("%b %d, %I:%M %p")

    conn = get_db_connection()

    conn.execute(
        'INSERT INTO notes (content, created_at) VALUES (?, ?)',
        (content, created_at)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Note added'})


# GET NOTES
@app.route('/get_notes')
def get_notes():

    conn = get_db_connection()

    notes = conn.execute(
        'SELECT * FROM notes ORDER BY id DESC'
    ).fetchall()

    conn.close()

    notes_list = []

    for note in notes:

        notes_list.append({
            'id': note['id'],
            'content': note['content'],
            'created_at': note['created_at']
        })

    return jsonify(notes_list)


# DELETE NOTE
@app.route('/delete_note/<int:id>', methods=['DELETE'])
def delete_note(id):

    conn = get_db_connection()

    conn.execute(
        'DELETE FROM notes WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Deleted'})


if __name__ == '__main__':
    app.run(debug=True)