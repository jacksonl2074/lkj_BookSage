import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Function to create the database and user table if they don't exist
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Home route
@app.route('/')
def index():
    # only this route doesn't work!
    return render_template('mainPage.html')

# Auth route for login/registration
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        if 'login' in request.form:
            email = request.form['email']
            password = request.form['password']
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = c.fetchone()
            conn.close()
            if user and check_password_hash(user[4], password):
                session['user_id'] = user[0]
                return redirect(url_for('profile'))
            else:
                flash('Invalid credentials')
        elif 'register' in request.form:
         first_name = request.form['first_name']
         last_name = request.form['last_name']
         email = request.form['email']
         password = request.form['password']
         confirm_password = request.form['confirm_password']
        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='scrypt')  # Updated method
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
                      (first_name, last_name, email, hashed_password))
                conn.commit()
                flash('Registration successful! Please login.')
                return redirect(url_for('auth'))
            except sqlite3.IntegrityError:
                flash('Email already exists.')
            finally:
              conn.close()
    else:
        flash('Passwords do not match')

    return render_template('auth.html')

# Profile route
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT first_name, last_name, email FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()
    conn.close()
    return render_template('profile.html', user=user)

# Logout route
# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('index'))
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))  # Redirects to the home page
if __name__ == '__main__':
    app.run(debug=True)
