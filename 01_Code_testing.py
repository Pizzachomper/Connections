import tkinter as tk

class Example(tk.Tk):
    def __init__(self):
        super().__init__()
        canvas = tk.Canvas(self)
        canvas.pack()
        self.hidebutton = tk.Button(canvas, text="Group button", background='white', font=("Helvetica"),
                                   command=lambda: self.hide_me(self.hidebutton))
        self.hidebutton.place(x=150, y=100)

    def hide_me(self, event):
        print('hide me')
        event.place_forget()

    def reappear(self, event):
        print("Reappear")
        event.place()

if __name__ == "__main__":
    Example().mainloop()