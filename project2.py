import tkinter as tk
import numpy as np
import os
import datetime

# ok so what im thinking for how we make the project extra is that we simulate whether you can survive off of gambling so we're gonna simulate the actions of a person and see if they starve to death or not -josh

class Simulation:
    def __init__(self):
        self.money = 110
        self.debt = 0
        self.day = 1
        self.hour = 0
        self.hunger = 1.0
        self.energy = 1.0

current_simulation = None

root = tk.Tk()
root.title("LETS GO GAMBLING!!!")
root.geometry("400x800")

label = tk.Label(root, text="Welcome to the Gambling Simulator!", font=("Times New Roman", 14))

output_label = tk.Label(root, text="", font=("Times New Roman", 12))

console_log = tk.Text(root, height=20, width=45, font=("Courier New", 12), bg="#0a192f", fg="white", insertbackground="white")

def disable_console_input(event):
    return "break"

console_log.bind("<Key>", disable_console_input)
console_log.bind("<Button-1>", disable_console_input)

console_messages = []

def redraw_console_log():
    console_log.config(state=tk.NORMAL)
    console_log.delete(1.0, tk.END)
    for msg_obj in console_messages:
        display_text = msg_obj['text']
        if msg_obj.get('count', 1) > 1:
            display_text += f" (x{msg_obj['count']})"
        start_index = console_log.index(tk.END)
        console_log.insert(tk.END, display_text + "\n")
        console_log.tag_add(msg_obj['color'], "end-%dc" % (len(display_text)+2), "end-1c")
        console_log.tag_config(msg_obj['color'], foreground=msg_obj['color'])
    console_log.see(tk.END)
    console_log.config(state=tk.DISABLED)

def add_log_message(msg, color="white"):
    if console_messages and console_messages[-1]['text'] == msg and console_messages[-1]['color'] == color:
        console_messages[-1]['count'] += 1
    else:
        console_messages.append({'text': msg, 'color': color, 'count': 1})
    redraw_console_log()

def clear_log():
    console_messages.clear()
    redraw_console_log()

# why did I make this an array and not a dictionary? -josh
# 0 - # combinations
# 1 - prize offset
# 2 - prize multiplier
# 3 - split chance
# 4 - title
outcomes_chart = [
    [39653068, 0, 0, 0, "You lose! Aw dangit!"],
    [850668, 1, 0, 0, "Mega Zeros."],
    [559650, 2, 0, 0, "Mega Ones."],
    [114800, 10, 0, 0, "Mega Twosies."],
    [223860, 8, 0, 0, "Regular Three."],
    [8610, 48, 0, 0, "Mega Three."],
    [5460, 0, 0.000003, 0.000131832, "Regular Four."],
    [210, 0, 0.00005, 0.000005070, "Mega Four."],
    [26, 0, 0.0005, 0.000000628, "Regular Five."],
    [1, 0, 1, 0.000000024, "ULTRA MEGA GRAND PRIZE!!!!!!!"],
]

def action_go_gambling(tickets = 1, grand_prize = 3000000):

    prize_money = 0
    odds_chart = [row[0] for row in outcomes_chart]
    total_outcomes = sum(odds_chart)
    
    outcomes = []
    for i in range(tickets):
        if total_outcomes <= 0:
            break
        r = np.random.randint(0, total_outcomes)
        cumulative = 0
        for idx, weight in enumerate(odds_chart):
            cumulative += weight
            if r < cumulative:
                odds_chart[idx] -= 1
                total_outcomes -= 1
                # not so sure about if this is how prize splitting works -josh
                shared = outcomes_chart[idx][2] > 0 and (outcomes_chart[idx][3] > np.random.rand())
                earnings = outcomes_chart[idx][1] + outcomes_chart[idx][2] * grand_prize * (0.5 if shared else 1)
                message = outcomes_chart[idx][4]
                if shared:
                    message += " Some other loser also won the jackpot, so they steal half of it!"
                if earnings > 0:
                    message += f" You won ${earnings}."
                add_log_message(message, "red" if earnings == 0 else "green")
                prize_money += earnings
                break

    return prize_money

status_box = tk.Text(root, height=10, width=45, font=("Courier New", 12), bg="#ffffff", fg="black", insertbackground="white")

def disable_status_input(event):
    return "break"

status_box.bind("<Key>", disable_status_input)
status_box.bind("<Button-1>", disable_status_input)

def redraw_status_box():
    status_box.config(state=tk.NORMAL)
    status_box.delete(1.0, tk.END)
    status_box.config(state=tk.DISABLED)

def export_log():
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"Logs/log_{now}.txt"
    log_text = console_log.get("1.0", tk.END).strip()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(log_text)
    output_label.config(text="log exported")

# Buttons
button_frame = tk.Frame(root)
generate_btn = tk.Button(button_frame, text="Generate Person", font=("Times New Roman", 12))
load_btn = tk.Button(button_frame, text="Load Person", font=("Times New Roman", 12))
start_btn = tk.Button(button_frame, text="Run Simulation", font=("Times New Roman", 12))
export_frame = tk.Frame(root)
export_log_btn = tk.Button(export_frame, text="Export Log", font=("Times New Roman", 12), command=export_log)
export_person_btn = tk.Button(export_frame, text="Export Person", font=("Times New Roman", 12))

def run_simulation():
    global current_simulation
    # Disable all buttons
    generate_btn.config(state=tk.DISABLED)
    load_btn.config(state=tk.DISABLED)
    start_btn.config(state=tk.DISABLED)
    export_log_btn.config(state=tk.DISABLED)
    export_person_btn.config(state=tk.DISABLED)

    current_simulation = Simulation()
    clear_log()
    output_label.config(text="simulation started")
    add_log_message("Hello world!")
    action_go_gambling(1,3000000)
    redraw_status_box()
    

    # End the simulation
    del current_simulation
    generate_btn.config(state=tk.NORMAL)
    load_btn.config(state=tk.NORMAL)
    start_btn.config(state=tk.NORMAL)
    export_log_btn.config(state=tk.NORMAL)
    export_person_btn.config(state=tk.NORMAL)

start_btn.config(command=run_simulation)

# --- PACK ALL WIDGETS AT THE BOTTOM ---
label.pack(pady=60)
button_frame.pack(pady=5)
generate_btn.pack(side=tk.LEFT, padx=5)
load_btn.pack(side=tk.LEFT, padx=5)
start_btn.pack(side=tk.LEFT, padx=5)
export_frame.pack(pady=5)
export_log_btn.pack(side=tk.LEFT, padx=5)
export_person_btn.pack(side=tk.LEFT, padx=5)
output_label.pack(pady=5)
status_box.pack(pady=10)
console_log.pack(pady=10)


root.mainloop()
