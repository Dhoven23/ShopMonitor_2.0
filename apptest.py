from tkinter import *
from tkinter import ttk
import tkinter

window = Tk()
style = ttk.Style()
style.theme_create('Cloud', settings={
    ".": {
        "configure": {
            "background": '#aeb0ce', # All colors except for active tab-button
            "font": 'red'
        }
    },
    "TNotebook": {
        "configure": {
            "background":'black', # color behind the notebook
            "tabmargins": [5, 5, 0, 0], # [left margin, upper margin, right margin, margin beetwen tab and frames]
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": 'dark blue', # Color of non selected tab-button
            "padding": [5, 2], # [space beetwen text and horizontal tab-button border, space between text and vertical tab_button border]
            "font":"white"
        },
        "map": {
            "background": [("selected", '#aeb0ce')], # Color of active tab
            "expand": [("selected", [1, 1, 1, 0])] # [expanse of text]
        }
    }
})
style.theme_use('Cloud')
note = ttk.Notebook(window)

window.tab1 = ttk.Frame(note)
window.tab2 = ttk.Frame(note)
window.tab3 = ttk.Frame(note)
window.tab4 = ttk.Frame(note)

note.add(window.tab1, text = "Home ")
note.add(window.tab2, text = "Disconnected ")
note.add(window.tab3, text = "Alarm ")
note.add(window.tab4, text = "")

note.pack()

window.mainloop()
