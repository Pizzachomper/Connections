import tkinter as tk

root = tk.Tk()

# Show and hides buttons depending on if the user has clicked a button before
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
body_font = ("Arial", "15")

# Group Button (Dropdown)
my_option_value = tk.StringVar()
my_option_value.set('Group 1')
my_option_menu = tk.OptionMenu(root, my_option_value, 'Group 1', 'Group 2', 'Group 3')
my_option_menu.config(width=20, font=body_font)

# Word Buttons
s_r_button = ShowHideButton(root, my_option_menu, text='Word Button')
s_r_button.config(width=20, font=body_font)

# Start Button
m_t_button = ShowHideButton(root, s_r_button, text='Start Game')
m_t_button.config(width=20, font=body_font)
m_t_button.pack()

root.mainloop()