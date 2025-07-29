from tkinter import *
from tkinter import ttk
from tkinter import messagebox # For error messages
import random
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.ticker import MultipleLocator # For setting Int tick intervals for Y axis of graph

# Global Variables #
running = False 
people = 0
# parameters
param_spawn_chance = 0
param_service_time_min = 0
param_service_time_max = 0
service_delay=0
time=0
served=0 # number of people served
ticks=0 # ticks of program for timing
serving = False # is someone being served
total_wait_time = 0 # cumulative wait time (for average wait time)
#plot data
people_data = [0]
time_data = [0]

# called by reset button
def reset():
    global people,service_delay,time,served,people_data,time_data,ticks
    people = 0
    service_delay = 0
    time=0
    served=0
    people_data = [0]
    time_data = [0]
    ticks=0
    average_wait_time = 0
    update_plot()
    draw()

def handleStartStop(startstopbutton):
    global running
    update_params()  
    if (param_spawn_chance > 0 and param_service_time_min > 0 and param_service_time_max > 0): # can't have 0 values
        running = not running
        if running:
            startstopbutton.config(text="Stop")
        else:
            startstopbutton.config(text="Start")
    else:
        messagebox.showerror("Cannot Start Simulation","Error: parameters must be entered")

# validate function for valid parameter inputs (ex/ rejects "foo")
def validate(v):  
    try:
        float(v)
        return True
    except:
        return False

# root
root = Tk()
root.title("Queue Simulation")
frm = ttk.Frame(root, padding=10)
frm.grid()
bar = ttk.Frame(frm)
bar.grid(column=0,columnspan=3,row=0,sticky='w')

# buttons / parameter input
startstopbutton = Button(bar, text="Start", command= lambda: handleStartStop(startstopbutton))
startstopbutton.pack(side="left")
Button(bar, text="Reset", command=reset).pack(side="left")
Label(bar, text="Spawn Chance(X/s):").pack(side="left")
entrySpawnChance = Entry(bar, width=4)
entrySpawnChance.pack(side="left")
Label(bar, text="Service Min(s):").pack(side="left")
entryServiceMin = Entry(bar, width=4)
entryServiceMin.pack(side="left")
Label(bar, text="Service Max(s):").pack(side="left")
entryServiceMax = Entry(bar, width=4)
entryServiceMax.pack(side="left")

# text box for real time stats
text_display = Text(root, height = 6, width = 52)
text_display.grid(column=0, columnspan=3, row=1, pady=10)
text_display.config(state="disabled") # dont allow editing of textbox

canvas = Canvas(frm, width=500, height=25, background='gray75')
canvas.grid(column=0,columnspan=3,row=2)

# plot graph
fig = Figure(figsize = (7, 6), dpi = 100)
plot1 = fig.add_subplot(111)
plot1.set_title("People in Queue Over Time")
plot1.set_xlabel("Seconds")
plot1.set_ylabel("People in Queue")

canvas2 = FigureCanvasTkAgg(fig,master = root)  
canvas2.draw()
canvas2.get_tk_widget().grid(column=0,row=2)

# No need to update parameters every tick, more efficent to update everytime start/stop button pressed. Allows for user to pause sim, update params, and resume.
def update_params():
    global param_service_time_max
    global param_service_time_min
    global param_spawn_chance
    global entryServiceMax
    global entryServiceMin
    global entrySpawnChance
    if (validate(entryServiceMax.get())):
        param_service_time_max = float(entryServiceMax.get()) or 0
    if (validate(entryServiceMin.get())):
        param_service_time_min = float(entryServiceMin.get()) or 0
    if (validate(entrySpawnChance.get())):
        param_spawn_chance = float(entrySpawnChance.get()) or 0
    # make sure entries are valid, change if not
    param_service_time_max = np.max([param_service_time_min,param_service_time_max])
    if (param_spawn_chance > 1):
        param_spawn_chance=1
    # update entry box text to match actual values for user
    entryServiceMin.delete(0,END)
    entryServiceMax.delete(0,END)
    entrySpawnChance.delete(0,END)
    entryServiceMin.insert(0,str(param_service_time_min))
    entryServiceMax.insert(0,str(param_service_time_max))
    entrySpawnChance.insert(0,str(param_spawn_chance))   

# Real time data collection
def update_text():
    global people,time,service_delay
    if (served > 0):
        average_wait_time = total_wait_time/(served+1)
    else:
        average_wait_time = 0
    text_display.config(state="normal")
    text_display.delete(1.0,END)
    # main text
    display_text = f"People: {people}\nTime: {time}s\nService Delay: {service_delay/20}s\nPeople Served: {served}\nTicks: {ticks}\nAverage Wait Time: {average_wait_time}s"
    text_display.insert(END,display_text)
    text_display.config(state="disabled")


def update_plot():
    global people
    global people_data
    global time_data

    # Better to create lists for people and time so graph is ascending to right instead of left
    people_data.append(people)
    time_data.append(time)
    
    plot1.clear()
    plot1.plot(time_data,people_data)
    plot1.set_title("People in Queue Over Time")
    plot1.set_xlabel("Seconds")
    plot1.set_ylabel("People in Queue")

    #y_locator = MultipleLocator(base=1.0)  # Only whole numbers
    #plot1.yaxis.set_major_locator(y_locator)
    canvas2.draw()
    update_text()  

# Queue Visual
def draw():
    global people
    canvas.delete("all")
    for i in range(people):
        canvas.create_rectangle(2+i*8, 2, i*8+7, 25, fill=("red" if i == 0 else "blue"))

# Runs every tick
def process():
    global running
    global service_delay
    global people
    global param_service_time_max
    global param_service_time_min
    global param_spawn_chance
    global served
    global serving
    global total_wait_time
    if not running:
        return
    # Use serving Boolean for setting serve time, previously it auto "served" a customer since serve_time starts at 0, so first customer had no wait
    if (people > 0):
        if (serving):
            service_delay-=1
            if (service_delay <= 0):
                serving = False
                people-=1
                served+=1
        else:
            serving = True
            service_delay = round(random.uniform(param_service_time_min,param_service_time_max)*20) # rng serve time
            total_wait_time+=(service_delay/20)         

# Use ticks to keep simulation consistently timed, it doesnt actually run 1-1 with real life due to added runtime but its simulated time is consistent
def loop():
    global running,ticks,people,time
    if running:
        process()
        draw()
        if(ticks%10 == 0):
            update_plot() # graph updates every 10 ticks (500ms)
            time+=0.5 
        if(ticks%20 == 0): # update every 1s
            # spawn customer rng
            if random.random() <= param_spawn_chance:
                people += 1
        ticks+=1
    root.after(50, loop) # 20 ticks/s 

loop()
reset()
root.mainloop()