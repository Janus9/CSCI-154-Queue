# Project I: Queue (Group 5)

# Libraries
import random
import matplotlib.pyplot as plt
import time
import numpy as np 

# 3. Initialize Variables that Hold Simulation Values
# / commented out variables not used
queue = []
#queue_free = True
ticks = 0
customers_served = 0
#total_wait = 0
running = False



        
# Setup Code including sim parameters
def main():
    global ticks, queue, customers_served
    # Initialize Variables that Require User Input
    print("Welcome to the Queue!")
    try:
        arrival_prob = float(input("Enter arrival probability (0 to 1): "))
        min_service_time = int(input("Enter MINIMUM service time (s): "))
        max_service_time = int(input("Enter MAXIMUM service time (s): "))
        simulation_time = int(input("Enter number of simulation steps(steps/s): "))
        interval = 1/simulation_time
    # Catch Invalid Input Types
    except ValueError:
        print("Invalid input: Use numbers only.")
        exit()

    # Error Checking for User Input
    if not (0 <= arrival_prob <= 1):
        print("Arrival probability must be between 0 and 1.")
        exit()
    elif min_service_time > max_service_time:
        print("Minimum service time can't be greater than maximum service time.")
        exit()
    elif min_service_time < 0 or max_service_time < 0:
        print("Service times must be greater than 0.")
        exit()
    elif max_service_time < min_service_time:
        print("Maximum service time can't be less than minimum service time.")
        exit()
    elif simulation_time <= 0:
        print("Simulation time must be greater than 0.")
        exit()
    running = True # sim running con
    being_served = False # is a customer currently being served
    serve_tick = 0 # how many ticks to serve a customer
    # Loop code, simulation_time / second   
    while running:
        try:
            # RNG for adding new customer to queue
            if (np.random.random() < arrival_prob):
                queue.append(ticks)
            # Creates serve time for customer
            if (not being_served and len(queue) > 0):
                serve_time = np.random.uniform(min_service_time, max_service_time) # time between serve min/max
                serve_tick = ticks+int(serve_time*simulation_time) # convert it into ticks so it can be used in real time sim
                being_served = True
                print("\n Customer serve time:", serve_time, "Will be served at tick:", serve_tick)
            # checks if serve_tick is reached
            if (being_served and ticks >= serve_tick):
                customer_id = queue.pop(0) 
                customers_served+=1
                being_served = False
                print("\nCustomer:", customer_id, "served!")
            print("\n",queue, "Ticks:", ticks, "Time:", ticks*interval,"(s)")
            time.sleep(interval)
            ticks+=1
        except KeyboardInterrupt:
            print("\nSimulation Stopped by User") # ctrl+c
            running = False

main()
# TLDR of changes
# I made a simple console design for it to showcase it running, the queue has a chance to add a customer every tick
# after serving a customer, sim decides random time between user input min/max for how long it takes to serve the new customer
# the sim time is ticks/second, so increasing this without decreasing the arrival_prob will increase the # of customers since its per tick



# 4. Loop over each time step
#   a. Decide if a customer arrives (use random)
#       - if yes, add them to the queue with their arrival time and service time
#   b. If the server is free and the queue is not empty:
#       - remove the next customer
#       - calculate their wait time
#       - update stats
#       - set the server as busy until service ends
#   c. Record the queue length at this time

# 5. After the loop:
# - calculate average wait time
# this is total wait time divided by customers served
# - print total customers served, average wait, etc.

# Resume, Pause, Start, End Controls in TKinter (not implemented here)

# 6. Plot the queue length over time using matplotlib
# - label axes, title, grid, and show the plot



# SIMULATION RULESET:
# Arrivals:
# Customers arrive randomly, controlled by an arrival probability per time unit (set by the user).
# Service:
#   There is a single server (e.g., cashier/teller).
#   Each customer’s service time is randomly chosen between a user-set minimum and maximum.
# Queue:
#   Arriving customers join the line.
#   The server serves the next customer in the queue when available.
#   When a customer is done being served, they leave the system.
# User Controls:
#   The simulation allows users to adjust:
#   Arrival probability
#   Minimum and maximum service times
#   Start, pause, and reset the simulation
# Visualization:
#   The simulation shows the queue as dots (customers) lined up, with the customer being served highlighted.
#   A live graph displays the queue length over time.
#   Live stats show time, number in queue, customers served, and average wait time