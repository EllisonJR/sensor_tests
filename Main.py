import time
import re
import Sensor
import SQLite
import tkinter as tk
import tk_tools
import collections
import numpy
from tkinter import ttk
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from datetime import datetime, timedelta

fig = plt.figure()
fig.set_size_inches(14, 4)
fig.canvas.toolbar.pack_forget()
ax = fig.add_subplot(1,1,1)
xs = []
ys = []

farenheitLabel = tk.Label()
farenheitLabel.place(relx=.10, rely=.01, anchor='ne')
celsiusLabel = tk.Label()
celsiusLabel.place(relx=.90, rely=.01, anchor='nw')

currentDateTime = datetime.now()
currentTime = datetime.now()
celsStr = ""

timerChoiceLabel1 = tk.Label()
timerChoiceLabel1.configure(text='Log to database every ')
timerChoiceLabel2 = tk.Label()
timerChoiceLabel2.configure(text=' minutes.')
timerChoiceLabel1.place(relx=.52, rely=.01, anchor='ne')
timerChoiceLabel2.place(relx=.70, rely=.01, anchor='ne')

timer_choice = ttk.Combobox(values=[5, 10, 15, 30])
timer_choice.place(relx=.65, rely=.01, anchor='ne')
timer_choice.current(0)

if timer_choice.current() == 0:
    DBtimer = int(5 * 60)
elif timer_choice.current() == 1:
    DBtimer = int(10 * 60)
elif timer_choice.current() == 2:
    DBtimer = int(15 * 60)
elif timer_choice.current() == 3:
    DBtimer = int(30 * 60)
    
DBinputTime = currentTime + timedelta(seconds=DBtimer)
print(DBtimer)

#pass in the xs/xy lists to use in animating the line plot for the time over temperature graph
def AnimateGraph(i, xs, ys):
    GrabSensorData()
    global celsStr
    
    xs.append(currentDateTime.strftime('%H:%M:%S'))
    
    xs = xs[-20:]
    ys = ys[-20:]
    
    ax.clear()
    ax.plot(xs, ys)
    
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Temperature Over Time')
    plt.ylabel('Temperature (Celsius)')
    ParseTime(celsStr)

#grabs data from sensor file, converts and stores it, displays each metric to its proper label
def GrabSensorData():
    global celsStr
    global currentDateTime
    
    temperatureInCelsius = round(Sensor.Readout(), 2)
    temperatureInFarenheit = round(((temperatureInCelsius * 1.8) + 32), 2)
    ys.append(temperatureInCelsius)
    farenStr = str(temperatureInFarenheit)
    celsStr = str(temperatureInCelsius)
    
    farenStr += 'F'+ u"\u00b0"
    celsStr += 'C' + u"\u00b0"
    
    celsiusLabel.configure(text=celsStr)
    farenheitLabel.configure(text=farenStr)
    
    currentDateTime = datetime.now()

#input timings for DB insertion
def ParseTime(celsStr):
    global DBtimer
    global DBinputTime
    global currentTime
    currentTime = datetime.now()
    if currentTime >= DBinputTime:
        SQLite.InsertData(celsStr)
        currentTime = datetime.now()
        DBinputTime = currentTime + timedelta(seconds=DBtimer)
        

#callback function for changing the sql logging timer
def Changetimer(arg):
    global DBtimer
    if timer_choice.current() == 0:
        DBtimer = int(5 * 60)
    elif timer_choice.current() == 1:
        DBtimer = int(10 * 60)
    elif timer_choice.current() == 2:
        DBtimer = int(15 * 60)
    elif timer_choice.current() == 3:
        DBtimer = int(30 * 60)

#main program loop
timer_choice.bind("<<ComboboxSelected>>", Changetimer)
ani = animation.FuncAnimation(fig, AnimateGraph, fargs=(xs, ys), interval=1000)
plt.show()
