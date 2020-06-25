import sqlite3
from datetime import datetime

def InsertData(temp):
    current = str(datetime.now())
    
    sqliteConnection = sqlite3.connect('SensorReadings.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("INSERT INTO temperature_readings(temperature, date) VALUES (?, ?)", (str(temp), current))
    sqliteConnection.commit();
    cursor.close()
    sqliteConnection.close()
