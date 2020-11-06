import tkinter as tk

root = tk.Tk()

prompt = tk.Entry(width = 12)
prompt.pack()

prompt.bind('<NUMPADENTER>')

root.mainloop()