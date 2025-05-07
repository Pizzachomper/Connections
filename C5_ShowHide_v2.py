import csv
import random
import tkinter as tk

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

word_1 = round_word_list[0]
word_2 = round_word_list[1]
word_3 = round_word_list[2]
word_4 = round_word_list[3]
word_5 = round_word_list[4]
word_6 = round_word_list[5]
word_7 = round_word_list[6]
word_8 = round_word_list[7]
word_9 = round_word_list[8]
word_10 = round_word_list[9]
word_11 = round_word_list[10]
word_12 = round_word_list[11]

group_1 = answer_list[0]
group_2 = answer_list[1]
group_3 = answer_list[2]

# Group and word lists
body_font = ("Arial", "15")

# Group Buttons (Dropdown)
group_option_value = tk.StringVar()
group_option_value.set(f"Group 1: {group_1}")
group_option_menu = tk.OptionMenu(root, group_option_value, f"Group 1: {group_1}", f"Group 2: {group_2}", f"Group 3: {group_3}")
group_option_menu.config(width=20, padx=5, pady=5, font=body_font)


# Word Buttons
word_button_4 = ShowHideButton(root, group_option_menu, text= f'{word_4}')
word_button_3 = ShowHideButton(root, word_button_4, text= f'{word_3}')
word_button_2 = ShowHideButton(root, word_button_3, text= f'{word_2}')
word_button = ShowHideButton(root, word_button_2, text= f'{word_1}')

word_button.config(width=22, padx=5, pady=5, font=body_font)
word_button_2.config(width=22, padx=5, pady=5, font=body_font)
word_button_3.config(width=22, padx=5, pady=5, font=body_font)
word_button_4.config(width=22, padx=5, pady=5, font=body_font)

# Start Button
start_button = ShowHideButton(root, word_button, text='Start Game')
start_button.config(width=22, padx=5, pady=5, font=body_font)
start_button.pack()

root.mainloop()