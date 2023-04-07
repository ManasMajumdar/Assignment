from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import datetime

def delete_expired_appointments():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("DELETE FROM appointments WHERE datetime(date || ' ' || time) < ?", (now,))
    conn.commit()
    conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_expired_appointments, trigger='interval', minutes=1)
scheduler.start()
