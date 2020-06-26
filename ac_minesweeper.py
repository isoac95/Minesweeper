import pprint
import tkinter as tk
from tkinter import messagebox
import time
import random


class Minesweeper:
    def __init__(self):
        self.size = {
            "Easy": [8, 10, 10],
            "Medium": [14, 18, 40],
            "Hard": [20, 24, 99]
        }
        self.colour_dict = {
            i: c for i, c in enumerate([
                "white", "blue", "green", "red", "purple",
                "cyan", "yellow", "magenta", "black"
            ])
        }
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root, bg="blue", padx=30, pady=2)
        self.start = time.time()
        self.choosen = tk.StringVar()
        self.choosen.set("Easy")
        self.choosen.trace("w", self.callback)
        self.reset()
        self.construct()
        self.clock()
        self.create_matrix(self.choosen.get())
        self.root.mainloop()

    def construct(self):
        self.root.title("MS by Ante Culo")
        self.root.configure(bg="blue")

        self.drop = tk.OptionMenu(self.root, self.choosen, "Easy", "Medium", "Hard")
        self.drop.config(bg="white", relief="flat", height=1, highlightthickness=0)

        self.marked = tk.Label(self.root, text="Marked: " + str(self.size[self.choosen.get()][2]),
                               relief='flat', bg="blue", fg="white")

        self.time_p = tk.Label(self.root, bg="blue", fg="white")

        self.time_p.pack()
        self.marked.pack()
        self.frame.pack()
        self.drop.pack(pady=5)

    def create_matrix(self, difficulty):
        nrows = self.size[difficulty][0]
        ncols = self.size[difficulty][1]
        nmine = self.size[difficulty][2]

        # Create a list where nmine elements have "mine" value,
        # while rest of the list elements have None value
        lst = ([None]*((nrows*ncols) - nmine) + ["mine"]*nmine)
        # Randomly shuffle list
        random.shuffle(lst)
        # From randomly shuffled list create matrix with nrows rows
        # and ncols columns
        self.matrix = [lst[i:i + ncols] for i in range(0, len(lst), ncols)]

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                neighbours = list()
                if self.matrix[i][j] != "mine":
                    chk_lst = ([
                        [i - 1, j - 1], [i - 1, j], [i - 1, j + 1], [i, j - 1],
                        [i, j + 1], [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]
                    ])
                    count = 0
                    for e in chk_lst:
                        if e[0] >= 0 and e[1] >= 0:
                            neighbours.append("i" + str(e[0]) + "j" + str(e[1]))
                        try:
                            if self.matrix[e[0]][e[1]] == "mine" and e[0] >= 0 and e[1] >= 0:
                                count += 1
                        except IndexError:
                            continue
                    self.matrix[i][j] = count
                name = "i" + str(i) + "j" + str(j)
                value = str(self.matrix[i][j])
                new_button = tk.Button(self.frame, relief="groove", height=1, width=2, bg="gray")
                data = [new_button, value, neighbours, i+j]
                self.dict_of_buttons[name] = data
                new_button.grid(row=i, column=j)
                new_button.bind('<Button-1>', lambda event, arg=name: self.left_click(event, arg))
                new_button.bind('<Button-3>', lambda event, arg=name: self.right_click(event, arg))
                # neighbours = list()
        pp = pprint.PrettyPrinter()
        pp.pprint(self.matrix)
        return self.matrix

    def left_click(self, event, arg):
        self.time_p.configure(fg="white")
        button = self.dict_of_buttons[arg][0]
        button_val = self.dict_of_buttons[arg][1]
        index = self.dict_of_buttons[arg][3]
        if button not in self.mark_buttons:
            if button_val != "mine":
                clr = self.colour_dict[int(button_val)]
                if index % 2 == 0:
                    button.configure(bg="white", text=button_val, fg=clr, relief="flat",
                                     state="disable", disabledforeground=clr)
                else:
                    button.configure(bg="gainsboro", text=button_val, fg="gainsboro", relief="flat",
                                     state="disable", disabledforeground=clr)
                if button not in self.open_buttons:
                    self.open_buttons.add(button)
                if button_val == "0":
                    button.configure(text="")
                    self.big_open(self.dict_of_buttons[arg][2])

            else:
                button.configure(fg="white", bg="red", text="M")
                self.open_buttons.add(button)
                self.time_p.configure(fg="blue")
                self.end_screen(button)
                answer = messagebox.askretrycancel("Mine! :(", "Better luck next time :P")
                if answer:
                    self.reset()
                    self.create_matrix(self.choosen.get())
                    self.marked.configure(text="Marked: " + str(self.size[self.choosen.get()][2]))
                    self.time_p.configure(fg="white")
                else:
                    exit()
            self.check_win()

    def right_click(self, event, arg):
        button = self.dict_of_buttons[arg][0]
        nmines = self.size[self.choosen.get()][2]
        if button not in self.open_buttons and button not in self.mark_buttons:
            if len(self.mark_buttons) < nmines:
                button.configure(fg="green", bg="green")
                self.mark_buttons.add(button)
            else:
                messagebox.showinfo("Warning!", "Too many marked fields!")

        elif button in self.mark_buttons:
            button.configure(fg="gray", bg="gray")
            self.mark_buttons.remove(button)

        self.marked.configure(text="Marked: " + str(nmines - len(self.mark_buttons)))
        self.check_win()

    def big_open(self, lst):
        for neighbour in lst:
            if neighbour in self.dict_of_buttons:
                nbutton = self.dict_of_buttons[neighbour][0]
                nvalue = self.dict_of_buttons[neighbour][1]
                clr = self.colour_dict[int(nvalue)]
                index = self.dict_of_buttons[neighbour][3]
                if (nvalue == "0" and nbutton not in self.open_buttons and
                   nbutton not in self.mark_buttons):
                    self.open_buttons.add(nbutton)
                    if index % 2 == 0:
                        nbutton.configure(bg="white", text="", relief="flat")
                    else:
                        nbutton.configure(bg="gainsboro", text="", relief="flat")

                    self.big_open(self.dict_of_buttons[neighbour][2])
                elif (nbutton not in self.open_buttons and
                      nvalue != "mine" and nbutton not in self.mark_buttons):
                    self.open_buttons.add(nbutton)

                    if index % 2 == 0:
                        nbutton.configure(bg="white", text=nvalue, relief="flat",
                                          fg=clr, disabledforeground=clr)
                    else:
                        nbutton.configure(bg="gainsboro", text=nvalue, relief="flat",
                                          fg=clr, disabledforeground=clr)

    def check_win(self):
        print(len(self.open_buttons) + len(self.mark_buttons))
        if len(self.open_buttons) + len(self.mark_buttons) == len(self.matrix)*len(self.matrix[0]):
            self.time_p.configure(fg="blue")
            messagebox.showinfo("Congratulations ;)", "Time: " + str(round(time.time()-self.start)))
            self.reset()
            self.create_matrix(self.choosen.get())
            self.marked.configure(text="Marked: " + str(self.size[self.choosen.get()][2]))
            self.time_p.configure(fg="white")

    def end_screen(self, stepped_on):
        for item in self.dict_of_buttons.items():
            button = item[1][0]
            value = item[1][1]
            if value == "mine" and button != stepped_on and button not in self.mark_buttons:
                button.configure(bg="orange", text="M", fg="white")
            elif value != "mine" and button in self.mark_buttons and button != stepped_on:
                button.configure(fg="red", text="X", bg="green2")

    def reset(self):
        self.dict_of_buttons = dict()
        self.mark_buttons = set()
        self.open_buttons = set()
        self.start = time.time()
        for widget in self.frame.winfo_children():
            widget.destroy()

    def clock(self):
        t = time.time()
        if t:
            self.time_p.config(text="Time: " + str(round(t-self.start)))
        self.root.after(100, self.clock)

    def callback(self, *args):
        print(self.choosen.get())
        size_m = self.choosen.get()
        self.reset()
        self.marked.configure(text="Marked: " + str(self.size[size_m][2]))
        if size_m == "Easy":
            self.create_matrix("Easy")
        elif size_m == "Medium":
            self.create_matrix("Medium")
        else:
            self.create_matrix("Hard")


if __name__ == '__main__':
    Minesweeper()
