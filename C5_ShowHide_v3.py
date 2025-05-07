import csv
import random
import tkinter as tk
from tkinter import *
from functools import partial  # To prevent unwanted windows

root = tk.Tk()

# Functions go here
def get_items():
    """
    Retrieves items from csv file in CSV folder in project folder
    Return: list of results where each list item has the correct name.
    """

    # Retrieve words from csv file and put them in a list
    file = open("03_Connections/Csv/connections_quiz.csv", "r")
    all_items = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row of headings
    all_items.pop(0)

    return all_items

def get_round_results():

    all_items_list = get_items()

    # Create lists to append items into
    all_results = []
    round_words = []
    round_before_after = []
    answer = []
    clue = []

    # loop until we have 3 different groups of items which arent duplicates
    while len(all_results) < 3:
        potential_items = random.choice(all_items_list)

        # Get the connections and check its not a duplicate question in a previous round
        if potential_items[5] not in answer:
            all_results.append(potential_items)
            round_before_after.append(potential_items[0])
            round_words.append(potential_items[1])
            round_words.append(potential_items[2])
            round_words.append(potential_items[3])
            round_words.append(potential_items[4])
            answer.append(potential_items[5])
            clue.append(potential_items[6])

    return all_results, round_before_after, round_words, answer, clue


# Show and hides buttons depending on if the user has clicked the button before
class ShowHideButton(tk.Button):

    # Code from Stack Overflow, DO NOT TOUCH!
    def __init__(self, parent, target_widget, *args, **kwargs):
        self.target = target_widget
        super().__init__(parent, *args, **kwargs)
        self.config(command=self.toggle)
    def toggle(self, force_off = False):
        if force_off or self.target.winfo_manager():
            self.target.pack_forget()
        else:
            self.target.pack()
        if isinstance(self.target, ShowHideButton):
            self.target.toggle(force_off=True)

# Main routine

# Get results from get round results function 
round_before_after_list = []
round_word_list = []
answer_list = []
clue_list = []

# get round word and groups
all_results, round_before_after_list, round_word_list, answer_list, clue_list = get_round_results()

play_box = Toplevel()

game_frame = Frame(play_box)
game_frame.grid(padx=10, pady=10)

# If users press the 'x' on the game window, end the entire game
play_box.protocol('WM_DELETE_WINDOW', root.destroy)

# Set up group buttons
group_frame = Frame(game_frame)
group_frame.grid(row=3)

group_button_ref = []

# Create 3 group buttons in a 3 by 1 grid
for item in range(0, 3):
    group_button = Button(group_frame, text="Group Name", width=21)

    group_button.grid(row= item // 3, column=item % 3, padx=5, pady=5)

# set up word buttons
word_frame = Frame(game_frame)
word_frame.grid(row=4)

word_button_ref = []

# # Create 12 word buttons in a 4 by 3 grid
for item in range(0, 12):
    word_button = Button(word_frame, text="Word Name", width=15)
    
    word_button.grid(row=item // 4, column=item % 4, padx=5, pady=5)

# Group and word lists
body_font = ("Arial", "15")
# config_preset = (width=20, padx=5, pady=5, font=body_font)

# Group Button (Dropdown)
my_option_value = tk.StringVar()
my_option_value.set("Group 1:")
my_option_menu = tk.OptionMenu(root, my_option_value, "Group 1: {group_1}", "Group 2: {group_2}", "Group 3: {group_3}")
my_option_menu.config(width=20, padx=5, pady=5, font=body_font)

# Word Buttons
s_r_button = ShowHideButton(root, my_option_menu, text= f'{word_frame}')
s_r_button.config(width=20, padx=5, pady=5, font=body_font)

# Start Button
m_t_button = ShowHideButton(root, s_r_button, text='Start Game')
m_t_button.config(width=20, padx=5, pady=5, font=body_font)
m_t_button.pack()

root.mainloop()