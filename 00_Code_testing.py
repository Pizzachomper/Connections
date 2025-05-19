import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows

play_box = Toplevel()

game_frame = Frame(play_box)
game_frame.grid(padx=10, pady=10)

# body font for most labels
body_font = ("Arial", "12")

# Set up group buttons
group_frame = Frame(game_frame)
group_frame.grid(row=3)

group_button_ref = []

# Create 3 group buttons in a 3 by 1 grid
for item in range(0, 3):
    group_button = Button(group_frame, font=body_font,
                                text="Group Name", width=21)
    group_button.grid(row= item // 3, column=item % 3, padx=5, pady=5)

def hide_me(event):
        print("hide (test)")
        event.widget.place_forget()

if body_font == ("Arial", "12"):
    group_button = hide_me()