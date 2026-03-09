import tkinter as tk
from tkinter import messagebox
import random

# --- Game Settings ---
cards = ['A','A','B','B','C','C','D','D']  # Can easily add more cards
random.shuffle(cards) #shuffle cards randomly

buttons = []
first_card = None #track the  first card
second_card = None #track the  second card
matched = 0   #count the  matched pairs
time_left = 30  #countdown  timer 
moves = 0

# --- Functions   to reser the puzzle game---
def reset_game():
    global cards, first_card, second_card, matched, time_left, moves
    cards = ['A','A','B','B','C','C','D','D']
    random.shuffle(cards)
    
    #reset the variable
    first_card = None  
    second_card = None  
    matched = 0  
    time_left = 30 
    moves = 0
    
    #update the UI labels
    timer_label.config(text=f"Time: {time_left}")
    moves_label.config(text=f"Moves: {moves}")
    status_label.config(text="Match all pairs!")
    
    #reset all the function button
    for btn in buttons:
        btn.config(text="?", state="normal", bg="#3498db")

# function  to check the match card
def check_match():
    global first_card, second_card, matched, moves

    moves += 1
    moves_label.config(text=f"Moves: {moves}")#update  moves  label

# check if  selected  cards match
    if cards[first_card] == cards[second_card]:
        buttons[first_card].config(bg="#2ecc71")  # Green for match
        buttons[second_card].config(bg="#2ecc71")
        matched += 1
        
        #check  if all pairs matched
        if matched == len(cards) // 2:
            status_label.config(text="🎉 You Win!")
            # Disable all buttons
            for btn in buttons:
                btn.config(state="disabled")
    else:
        buttons[first_card].after(300, lambda: buttons[first_card].config(text="?"))
        buttons[second_card].after(300, lambda: buttons[second_card].config(text="?"))
# reset  selected cards
    first_card = None
    second_card = None
    # Re-enable unmatched buttons
    for btn in buttons:
        if btn["text"] == "?":
            btn.config(state="normal")

#function for card  click
def click_card(i):
    global first_card, second_card
 
 #only allow  flipping  if card is  face -down and second card  not yet selected
    if buttons[i]["text"] == "?" and second_card is None:
        buttons[i].config(text=cards[i], bg="#f1c40f")  # Yellow when flipped
        if first_card is None:
            first_card = i  #set first  selected card
        elif second_card is None:
            second_card = i #set second selected card
            
            
            # temporarily disable  all button  to prevent  extra click
            for btn in buttons:
                btn.config(state="disabled")
            # Check match after 500ms
            root.after(500, check_match)
            
            
# countdown the  function
def countdown():
    global time_left
    if matched == len(cards) // 2:
        return  # Stop timer if game is won
    if time_left > 0:
        time_left -= 1 # decrease  time
        timer_label.config(text=f"Time: {time_left}")
        root.after(1000, countdown)# call countdown every 1 second
    else:
        status_label.config(text="⏰ Time Over!") #display  over the  time
        
        #disale  all buttons
        for btn in buttons:
            btn.config(state="disabled")

# --- UI Setup ---
root = tk.Tk()
root.title("Memory Puzzle Game")
root.geometry("450x400")
root.configure(bg="#34495e")

# --- Labels   for  timer  ., moves and status---
timer_label = tk.Label(root, text=f"Time: {time_left}", font=("Arial", 14), fg="white", bg="#34495e")
timer_label.grid(row=0, column=0, columnspan=2, pady=10)

moves_label = tk.Label(root, text=f"Moves: {moves}", font=("Arial", 14), fg="white", bg="#34495e")
moves_label.grid(row=0, column=2, columnspan=2, pady=10)

status_label = tk.Label(root, text="Match all pairs!", font=("Arial", 12), fg="white", bg="#34495e")
status_label.grid(row=1, column=0, columnspan=4, pady=5)

# ---  create   card Buttons ---
for i in range(len(cards)):
    btn = tk.Button(root, text="?", width=8, height=4,
                    font=("Arial", 14, "bold"),
                    bg="#3498db", fg="white",
                    activebackground="#2980b9",
                    command=lambda i=i: click_card(i))# bind click the  function
    btn.grid(row=2 + i//4, column=i%4, padx=5, pady=5) #arrange the grid
    buttons.append(btn)

# --- Restart Button ---
restart_btn = tk.Button(root, text="Restart Game", font=("Arial", 12, "bold"),
                        bg="#e74c3c", fg="white", activebackground="#c0392b",
                        command=reset_game)
restart_btn.grid(row=4, column=0, columnspan=4, pady=15)

# Start countdown
countdown() #
root.mainloop()