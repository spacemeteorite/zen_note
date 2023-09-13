'''User created widgets'''
import tkinter as tk
from tkinter import ttk


class TocUnitFrame(ttk.Frame):
    def __init__(self, master, title, summary, creation_time, last_update_time, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title = ttk.Label(self, text=title)
        self.summary = ttk.Label(self, text=summary)
        self.creation_time = ttk.Label(self, text=creation_time)
        self.last_update_time = ttk.Label(self, text=last_update_time)

        self.title.grid(row=0)
        self.summary.grid(row=1, column=0)
        self.creation_time.grid(row=1, column=1)
        self.last_update_time.grid(row=1, column=2)



app = tk.Tk()
TocUnitFrame(app, 'hello', 'world', 'hello', 'hello', relief='solid', borderwidth=5).grid()
app.mainloop()