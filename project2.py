import tkinter as tk
import numpy as np
import os
import datetime

you_lose = False

class Simulation:
    def __init__(self):
        self.config_interest_rate = 0.005
        self.config_tickets_mean = 10
        self.config_tickets_scale = 5

        self.money = 110.0
        self.debt = 0.0
        self.day = 1
        self.hour = 0
        self.hunger = 1.0
        self.energy = 1.0
        self.food = 1.0
        self.hunger = 1.0
        self.energy = 1.0
        
        self.stat_money_earned_by_gambling = 0.0
        self.stat_money_earned_by_working = 0.0
        self.stat_money_stolen = 0.0
        self.stat_expenditures = 0.0
        self.stat_stolen_from = 0.0

current_simulation = None

root = tk.Tk()
root.title("LETS GO GAMBLING!!!")
root.geometry("400x800")

label = tk.Label(root, text="Welcome to the Gambling Simulator!", font=("Times New Roman", 14))

output_label = tk.Label(root, text="", font=("Times New Roman", 12))

input_label = tk.Label(root, text="num_tickets,jackpot,iterations", font=("Times New Roman", 12))
input_textbox = tk.Entry(root, font=("Times New Roman", 12), width=20)

console_log = tk.Text(root, height=30, width=45, font=("Courier New", 12), bg="#0a192f", fg="white", insertbackground="white")

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

def tksleep(t):
    ms = int(t*1000)
    root = tk._get_default_root('sleep')
    var = tk.IntVar(root)
    root.after(ms, var.set, 1)
    root.wait_variable(var)

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
    [1, 0, 1, 0.000000024, "WIN!!!"],
]

def action_eat_food(sim: Simulation):
    amnt_to_eat = np.min([1.0 - sim.hunger, sim.food])
    sim.hunger += amnt_to_eat
    sim.food -= amnt_to_eat
    add_log_message(f"You decided to eat {amnt_to_eat} food units of food")

def action_work(sim: Simulation):
    earnings = int(np.floor(np.max([np.random.normal(loc=16,scale=3,size=(1))[0],0])))
    add_log_message(f"You did some doordash deliveries and made ${earnings}!")
    sim.money += earnings
    sim.stat_money_earned_by_working += earnings
    taxes = earnings * 0.09
    add_log_message(f"You paid the working tax and lost ${taxes}")
    sim.money -= taxes
    sim.stat_stolen_from -= taxes

def action_steal_low_risk(sim: Simulation):
    global you_lose
    if np.random.rand() > 0.998:
        you_lose = True
        add_log_message(f"You tried to rob someone but they shot you in the face. YOU DIED", "red")
        return
    rand = np.random.rand()
    earnings = 0
    if rand < 0.3:
        earnings = int(np.floor(np.max([np.random.normal(loc=150,scale=150,size=(1))[0],0])))
        add_log_message(f"You stole some packages on someones porch were able to sell them for ${earnings}")
    if rand < 0.6:
        earnings = int(np.floor(np.max([np.random.normal(loc=25,scale=10,size=(1))[0],0])))
        add_log_message(f"You mugged some random guy and got ${earnings}")
    if rand < 1.0:
        earnings = int(np.floor(np.max([np.random.normal(loc=2,scale=1,size=(1))[0],0])))
        add_log_message(f"You stole some candy from a baby and flipped it for ${earnings}")
    sim.money += earnings
    sim.stat_money_stolen += earnings

def action_steal_high_risk(sim: Simulation):
    global you_lose
    if np.random.rand() > 0.01:
        you_lose = True
        add_log_message(f"You tried to commit a robbery with a deadly weapon and were arrested. GAME OVER", "red")
        return
    rand = np.random.rand()
    earnings = 0
    if rand < 0.4:
        earnings = int(np.floor(np.max([np.random.normal(loc=2000,scale=1000,size=(1))[0],0]))) 
        add_log_message(f"You robbed a gas station and got some money!!! +${earnings}!")
    if rand < 0.7:
        earnings = int(np.floor(np.max([np.random.normal(loc=37500,scale=10000,size=(1))[0],0]))) 
        add_log_message(f"You robbed a bank and got some money!!! +${earnings}!")
    if rand < 1.0:
        earnings = int(np.floor(np.max([np.random.normal(loc=25000,scale=7500,size=(1))[0],0]))) 
        add_log_message(f"You robbed a jewlery store and got some money!!! +${earnings}!")
    sim.money += earnings
    sim.stat_money_stolen += earnings

def action_sleep(sim: Simulation):
    add_log_message("You took an hour long nap")
    sim.energy = np.min([sim.energy + 0.125, 1])

def action_buy_food(sim: Simulation):
    amnt_to_buy = np.clip(a=np.random.normal(loc=7,scale=3,size=(1))[0],a_min=0.0,a_max=7.0-sim.food)
    cost = amnt_to_buy * 16.80 
    add_log_message(f"You went to the store and bought {amnt_to_buy} food units of food for ${cost}.")
    sim.food += amnt_to_buy
    sim.money -= cost
    sim.stat_expenditures -= cost
    taxes = cost * 0.085 
    add_log_message(f"You paid the buying groceries tax and lost ${taxes}")
    sim.money -= taxes
    sim.stat_stolen_from -= taxes


def action_do_nothing(sim: Simulation):
    add_log_message(np.random.choice([
        "You sat and did nothing",
        "You clapped your hands and bounced up and down",
        "You did a little dance",
        "You thought about something better to do",
        "You thought about what you'll do with the money you win when you strike it big",
        "You got bored",
        "You thought about nothing in particular",
        "You twirled around",
        "You made a bunch of funny noises with your mouth",
        ]))

def action_go_gambling(tickets = 1, grand_prize = 3000000, silent = False):

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
                # this is exactly how prize splitting works -josh
                shared = outcomes_chart[idx][2] > 0 and (outcomes_chart[idx][3] > np.random.rand())
                earnings = outcomes_chart[idx][1] + outcomes_chart[idx][2] * grand_prize * (0.5 if shared else 1)
                if not silent:
                    message = outcomes_chart[idx][4]
                    if shared:
                        message += " Some other loser also won the jackpot, so they steal half of it!"
                    if earnings > 0:
                        message += f" You won ${earnings}."
                    add_log_message(message, "red" if earnings == 0 else "green")
                prize_money += earnings
                break

    return prize_money

# arrays once again. 
# [0] - weight function (must be deterministic)
# [1] - action function
actions = [
    [lambda sim: 1.0, action_do_nothing],
    [lambda sim: 7.0-sim.food, action_buy_food],
    [lambda sim: 100 if sim.hunger <= 0.66 and sim.food > 0 else 0, action_eat_food],
    [lambda sim: np.max([0,(sim.energy-0.7) * -400]), action_sleep],
    [lambda sim: 0.5 + np.max([0,sim.money * -1]), action_work],
    [lambda sim: np.max([0,(sim.money) * -0.5]), action_steal_low_risk],
    [lambda sim: np.max([0,(sim.money+1000) * -0.25]), action_steal_high_risk],
]

def do_action():
    global actions
    global current_simulation
    total = 0.0
    for action in actions:
        total += action[0](current_simulation)
    rand = np.random.rand() * total
    n = 0
    for action in actions:
        n += action[0](current_simulation)
        if (rand < n):
            action[1](current_simulation)
            break

status_box = tk.Text(root, height=15, width=45, font=("Courier New", 12), bg="#ffffff", fg="black", insertbackground="white")

def disable_status_input(event):
    return "break"

status_box.bind("<Key>", disable_status_input)
status_box.bind("<Button-1>", disable_status_input)

def redraw_status_box():
    global current_simulation
    status_box.config(state=tk.NORMAL)
    status_box.delete(1.0, tk.END)
    status_box.insert(tk.END, f"Day {current_simulation.day} {current_simulation.hour}h" + "\n")
    status_box.insert(tk.END, f"-POSSESIONS-" + "\n")
    status_box.insert(tk.END, f"MONEY : ${current_simulation.money}" + "\n")
    status_box.insert(tk.END, f"FOOD  : {current_simulation.food}" + "\n")
    status_box.insert(tk.END, f"-ATTRIBUTES-" + "\n")
    status_box.insert(tk.END, f"ENERGY: {current_simulation.energy}" + "\n")
    status_box.insert(tk.END, f"HUNGER: {current_simulation.hunger}" + "\n")
    status_box.insert(tk.END, f"-STATISTICS-" + "\n")
    status_box.insert(tk.END, f"EARNINGS FROM GAMBLING: ${current_simulation.stat_money_earned_by_gambling}" + "\n")
    status_box.insert(tk.END, f"EARNINGS FROM WORKING: ${current_simulation.stat_money_earned_by_working}" + "\n")
    status_box.insert(tk.END, f"EARNINGS FROM STEALING: ${current_simulation.stat_money_stolen}" + "\n")
    status_box.insert(tk.END, f"EXPENDITURES: ${current_simulation.stat_expenditures}" + "\n")
    status_box.insert(tk.END, f"SEIZED BY GOVERNMENT: ${current_simulation.stat_stolen_from}" + "\n")
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
start_btn2 = tk.Button(button_frame, text="Simulate ticket buying", font=("Times New Roman", 12))
export_frame = tk.Frame(root)
export_log_btn = tk.Button(button_frame, text="Export Log", font=("Times New Roman", 12), command=export_log)
export_person_btn = tk.Button(export_frame, text="Export Person", font=("Times New Roman", 12))

def run_simulation_2(input_tickets = 1, input_jackpot = 30000000, input_iterations = 1, silent = False):
    try:
        input_values = input_textbox.get().strip().split(',')
        if len(input_values) >= 1 and input_values[0].strip():
            input_tickets = int(float(input_values[0].strip()))
        if len(input_values) >= 2 and input_values[1].strip():
            input_jackpot = int(input_values[1].strip())
        if len(input_values) >= 3 and input_values[2].strip():
            input_iterations = int(float(input_values[2].strip()))
            
        add_log_message(f"Lets go gambling {input_iterations} times!", "yellow")
        
        total_prize = 0
        total_cost = input_tickets * 5 * input_iterations
        
        for i in range(input_iterations):
            prize = action_go_gambling(input_tickets, input_jackpot, True)
            total_prize += prize
            
        avg_prize = total_prize / input_iterations
        net_gain = total_prize - total_cost
        avg_net_gain = net_gain / input_iterations
        roi = (total_prize / total_cost) - 1 if total_cost > 0 else -1
        
        if not silent:
            add_log_message(f"Average prize per iteration: ${avg_prize:.2f}", "cyan")
            add_log_message(f"Average net gain per iteration: ${avg_net_gain:.2f}", "cyan")
            add_log_message(f"Average ROI: {roi:.4f}", "cyan")
        
        return roi
    except ValueError:
        add_log_message("Error: Please enter valid numbers in the textbox!", "red")
        return

def run_simulation():
    global current_simulation
    global you_lose
    you_lose = False
    # Disable all buttons
    generate_btn.config(state=tk.DISABLED)
    load_btn.config(state=tk.DISABLED)
    start_btn.config(state=tk.DISABLED)
    start_btn2.config(state=tk.DISABLED)
    export_log_btn.config(state=tk.DISABLED)
    export_person_btn.config(state=tk.DISABLED)

    current_simulation = Simulation()
    clear_log()
    add_log_message(f"Day {current_simulation.day}")
    add_log_message("Hello world!")
    
    
    while current_simulation.day < 30 and you_lose == False:
        current_simulation.hour += 1
        # lets lose some stats!
        current_simulation.energy -= 0.04
        current_simulation.hunger -= 0.04
        # it's been a day?
        if current_simulation.hour == 24:
            #inflation
            inflation = current_simulation.money * 0.000074
            current_simulation.money -= inflation
            current_simulation.stat_stolen_from -= inflation
            add_log_message(f"You paid the inflation tax and lost ${inflation}!", "yellow")
            #time increment
            current_simulation.hour = 0
            current_simulation.day += 1
            #lets go gambling!
            jackpot = np.floor(np.max([np.random.normal(loc=15000000,scale=10000000,size=(1))[0],7000000]))
            tickets = int(np.floor(np.max([np.random.normal(loc=current_simulation.config_tickets_mean,scale=current_simulation.config_tickets_scale,size=(1))[0],0])))
            ticketcost = tickets * 5
            add_log_message(f"[[[Lets go gambling!]]]", "yellow")
            add_log_message(f"The jackpot is ${jackpot}. You've decided to buy {tickets} tickets for ${ticketcost}.", "yellow")
            current_simulation.money -= ticketcost
            current_simulation.stat_money_earned_by_gambling -= ticketcost
            winnings = action_go_gambling(tickets,jackpot)
            current_simulation.money += winnings
            current_simulation.stat_money_earned_by_gambling += winnings
            add_log_message(f"You won ${winnings}!", "yellow")
            if winnings > 0:
                gambling_tax = float(winnings) * 0.35
                current_simulation.money -= gambling_tax
                current_simulation.stat_stolen_from -= gambling_tax
                add_log_message(f"You paid the winning tax and lost ${gambling_tax}!", "yellow")
            if current_simulation.money < 0:
                interest = current_simulation.money * current_simulation.config_interest_rate
                add_log_message(f"Your loan gained ${interest} in interest!", "yellow")
                current_simulation.money += interest

            add_log_message(f"[[[Day {current_simulation.day}]]]", "magenta")
        
        # do your hourly action
        do_action()
        # potentially die
        if current_simulation.hunger < -4.00:
            you_lose = True
            add_log_message(f"You died of starvation", "red")
        if current_simulation.energy < -4.00:
            you_lose = True
            add_log_message(f"You died of exhaustion", "red")
        
        redraw_status_box()
        tksleep(0.01)
        
    

    # End the simulation
    del current_simulation
    generate_btn.config(state=tk.NORMAL)
    load_btn.config(state=tk.NORMAL)
    start_btn.config(state=tk.NORMAL)
    start_btn2.config(state=tk.NORMAL)
    export_log_btn.config(state=tk.NORMAL)
    export_person_btn.config(state=tk.NORMAL)

start_btn.config(command=run_simulation)
start_btn2.config(command=run_simulation_2)

# --- PACK ALL WIDGETS AT THE BOTTOM ---
label.pack(pady=5)
input_label.pack(pady=2)
input_textbox.pack(pady=2)
button_frame.pack(pady=5)
#generate_btn.pack(side=tk.LEFT, padx=5)
#load_btn.pack(side=tk.LEFT, padx=5)
export_log_btn.pack(side=tk.LEFT, padx=5)
start_btn.pack(side=tk.LEFT, padx=5)
start_btn2.pack(side=tk.LEFT, padx=5)
#export_person_btn.pack(side=tk.LEFT, padx=5)
output_label.pack(pady=0)
status_box.pack(pady=0)
console_log.pack(pady=0)

#jackpots = [10,7000000,30000000,1000000000]
#tickets_bought = [1,10,1000,1000000]
#array = [[0 for _ in range(4)] for _ in range(4)]
#
#for j in range(4):
#    for t in range(4):
#        print(j,t)
#        array[j][t] = run_simulation_2(tickets_bought[t],jackpots[j],100,True)
#
#print(array)

root.mainloop()
