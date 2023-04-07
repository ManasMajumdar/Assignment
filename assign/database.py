import sqlite3

conn = sqlite3.connect('appointments.db')
c = conn.cursor()

# create the users table
c.execute('''CREATE TABLE users
             (email text, password text)''')

# create the appointments table
c.execute('''CREATE TABLE appointments
             (id integer primary key autoincrement,
              name text, date text, time text, description text)''')

conn.commit()
conn.close()
