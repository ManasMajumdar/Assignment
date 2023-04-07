import scheduler

from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import bcrypt
import sqlite3
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
      app.run(debug=True)


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def save(self):
        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?)", (self.email, self.password))
        conn.commit()
        conn.close()

    @staticmethod
    def get(email):
        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        row = c.fetchone()
        if row:
            return User(row[0], row[1])
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')
import bcrypt

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def save(self):
        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?)", (self.email, self.password))
        conn.commit()
        conn.close()
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/appointments')
def appointments():
    if 'email' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("SELECT * FROM appointments WHERE date >= DATE('now') ORDER BY date, time")
    rows = c.fetchall()
    appointments = [dict(id=row[0], name=row[1], date=row[2], time=row[3], description=row[4]) for row in rows]
    conn.close()

    return render_template('appointments.html', appointments=appointments)

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    if 'email' not in session:
        return redirect(url_for('login'))

   
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    if 'email' not in session:
        return redirect(url_for('login'))

    name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    description = request.form['description']

    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("INSERT INTO appointments (name, date, time, description) VALUES (?, ?, ?, ?)", (name, date, time, description))
    conn.commit()
    conn.close()

    return redirect(url_for('appointments'))

@app.route('/delete_appointment/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    if 'email' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
    conn.commit()
    conn.close()

    return ('', 204)
