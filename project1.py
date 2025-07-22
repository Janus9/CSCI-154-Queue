from tkinter import *
from tkinter import ttk
import random
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

running = False
people = 0
plot_length = 120
plot_data = [0 for i in range(plot_length)]
param_spawn_chance = 0.1
param_service_time_min = 0.5
param_service_time_max = 1.5
service_delay=0


def reset():
    global people
    global service_delay
    global plot_data
    people = 0
    service_delay = 0
    plot_data = [0 for i in range(plot_length)]

def handleStartStop(startstopbutton):
    global running
    running = not running
    if running:
        startstopbutton.config(text="Stop")
    else:
        startstopbutton.config(text="Start")

def handleReset():
    reset()

def validate(v):
    try:
        float(v)
        return True
    except:
        return False


root = Tk()
root.title("!!!!!!!!!!!!!!!!!SIMULATION!!!!!!!!!!!!!!!!!!!!!!!!!")
frm = ttk.Frame(root, padding=10)
frm.grid()

bar = ttk.Frame(frm)
bar.grid(column=0,columnspan=3,row=0,sticky='w')

startstopbutton = Button(bar, text="Start", command= lambda: handleStartStop(startstopbutton))
startstopbutton.pack(side="left")
Button(bar, text="Reset", command=handleReset).pack(side="left")
Label(bar, text="spawn chance:").pack(side="left")
entrySpawnChance = Entry(bar, width=4)
entrySpawnChance.pack(side="left")
Label(bar, text="service min:").pack(side="left")
entryServiceMin = Entry(bar, width=4)
entryServiceMin.pack(side="left")
Label(bar, text="service max:").pack(side="left")
entryServiceMax = Entry(bar, width=4)
entryServiceMax.pack(side="left")

canvas = Canvas(frm, width=500, height=25, background='gray75')
canvas.grid(column=0,columnspan=3,row=1)

fig = Figure(figsize = (5, 5), dpi = 100)

plot1 = fig.add_subplot(111)

plot1.plot(plot_data)

canvas2 = FigureCanvasTkAgg(fig,master = root)  
canvas2.draw()

canvas2.get_tk_widget().grid(column=0,row=2)

# this shit runs every goddamn frame
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
    param_service_time_max = np.max([param_service_time_min,param_service_time_max])

def update_plot():
    global running
    if running:
        global plot_data
        global people
        global plot_length
        newv = people
        # this shit bad
        plot_data.insert(0,newv)
        plot_data.pop(plot_length)
        plot1.clear()
        plot1.plot(plot_data)
        canvas2.draw()
    root.after(500, update_plot)
update_plot()

def draw():
    global people
    canvas.delete("all")
    for i in range(people):
        canvas.create_rectangle(2+i*8, 2, i*8+7, 25, fill=("red" if i == 0 else "blue"))

def process():
    global running
    global service_delay
    global people
    global param_service_time_max
    global param_service_time_min
    global param_spawn_chance
    if not running:
        return
    if people > 0:
        service_delay -= 0.05
        while service_delay < 0 and people > 0:
            service_delay += param_service_time_min + random.random()*(param_service_time_max-param_service_time_min)
            people -= 1
    if random.random() < param_spawn_chance:
        people += 1

def loop():
    update_params()
    process()
    draw()
    root.after(50, loop)

loop()

reset()

root.mainloop()

# team name ideas

# team funny
# stupid idiot team
# team sigma
# gods chosen people
# team minecraft
# ultrawinners
# ultralosers
# team 5
# team 7
# VEVBTSBVTFRSQUNPT0w=
# asldfhphpu
# team "Five"
# team chatgpt
# johnny simulation and the simulation guys
