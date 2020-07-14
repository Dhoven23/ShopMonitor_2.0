from tkinter import Button, Tk, DISABLED

root = Tk()





class ToolButton:
    button = Button()
    def __init__(self, master, x, y):
        def Onclick():
            print(number)
        number = x * y
        self.button = Button(master, text=str(number), width=20, command=Onclick)
        self.button.grid(column=x, row=y)
        print(self.button)







def main():
    for x in range(1, 5):
        for y in range(1, 5):
            ToolButton.__init__(ToolButton,root, x, y)


if __name__ == '__main__':
    main()
    root.mainloop()
