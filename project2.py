import tkinter as tk
import numpy as np

root = tk.Tk()
root.title("LETS GO GAMBLING!!!")
root.geometry("400x400")

label = tk.Label(root, text="Welcome to the Gambling Simulator!", font=("Times New Roman", 14))
label.pack(pady=60)

output_label = tk.Label(root, text="", font=("Times New Roman", 14))
output_label.pack(pady=10)

# why did I make this an array and not a dictionary? -josh
# 0 - chance
# 1 - prize offset
# 2 - prize multiplier
# 3 - split chance
# 4 - title
the_odds = [
    [0.020539423, 1, 0, 0, "Mega Zeros"],
    [0.013512778, 2, 0, 0, "Mega Ones"],
    [0.002771852, 10, 0, 0, "Mega Twosies"],
    [0.005405111, 8, 0, 0, "Regular Three"],
    [0.000207889, 48, 0, 0, "Mega Three"],
    [0.000131832, 0, 0.000003, 0.000131832, "Regular Four"],
    [0.000005070, 0, 0.00005, 0.000005070, "Mega Four"],
    [0.000000628, 0, 0.0005, 0.000000628, "Regular Five"],
    [0.000000024, 0, 1, 0.000000024, "ULTRA MEGA GRAND PRIZE!!!!!!!"],
]

def go_gambling():
    money = 0
    chance = 0
    prize = None
    r = np.random.rand()
    for i in range(len(the_odds)):
        chance += the_odds[i][0]
        if r <= chance:
            money = the_odds[i][1]
            prize = i
            break
    if prize is not None:
        output_label.config(text=f"You won! You won {the_odds[prize][4]} and got {money} dollars")
    else:
        output_label.config(text=f"You lost! Aw dangit!")
    return money

button = tk.Button(root, text="Lets go gambling!", font=("Times New Roman", 12), command=go_gambling)
button.pack(pady=10)

root.mainloop()
