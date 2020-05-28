import pprint
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import time
import random

class Minesweeper:
    def __init__(self):
        self.dict_of_buttons = dict()
        self.mark_buttons = list()
        self.open_buttons = list()
        self.size = {"Easy" : [8, 10, 10], "Medium" : [14, 18, 40], "Hard" : [20, 24, 99]}
        self.colour_dict = {0 : "white", 1 : "blue", 2 : "green", 3 : "red", 4 : "purple", 5 : "cyan", 6 : "yellow", 7 : "magenta", 8 : "black"}
        self.matrix = [[]]
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root, bg="blue", padx=30, pady=2)
        self.start = time.time()
        self.choosen = StringVar()
        self.choosen.set("Easy")
        self.choosen.trace("w", self.callback)
        self.construct()
        self.clock()
        self.create_matrix(self.choosen.get())
        self.close()

    def construct(self):
        self.root.title("MS by Ante Culo")
        self.root.configure(bg="blue")

        self.drop = OptionMenu(self.root, self.choosen, "Easy", "Medium", "Hard")
        self.drop.config(bg="white", relief="flat", height=1)

        self.marked = tk.Label(self.root, text="Marked: " + str(self.size[self.choosen.get()][2]), relief='flat', bg="blue", fg="white")

        self.time_p = tk.Label(self.root, bg="blue", fg="white")

        self.time_p.pack()
        self.marked.pack()
        self.frame.pack()
        self.drop.pack()

    def create_matrix(self, difficulty):
        lst = ([None] * ((self.size[difficulty][0] * self.size[difficulty][1]) - self.size[difficulty][2])
        + ["mine"] * self.size[difficulty][2])

        random.shuffle(lst)
        n = self.size[difficulty][1]
        self.matrix = [lst[i:i + n] for i in range(0, len(lst), n)]

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                neighbours = list()
                if self.matrix[i][j] != "mine":
                    chk_lst = ([[i - 1, j - 1], [i - 1, j], [i - 1, j + 1], [i, j - 1],
                    [i, j + 1], [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]])
                    count = 0
                    for element in chk_lst:
                        if element[0] >= 0 and element[1] >= 0:
                            neighbours.append("i" + str(element[0]) + "j" + str(element[1]))
                        try:
                            if self.matrix[element[0]][element[1]] == "mine" and element[0] >= 0 and element[1] >= 0:
                                count += 1
                        except IndexError:
                            continue
                    self.matrix[i][j] = count
                name = "i" + str(i) + "j" + str(j)
                num = str(self.matrix[i][j])
                self.dict_of_buttons[name] = [tk.Button(self.frame, relief="groove", height=1, width=2, fg = "gray", bg="gray"), num, neighbours, i+j]
                self.dict_of_buttons[name][0].grid(row=i, column=j)
                self.dict_of_buttons[name][0].bind('<Button-1>', lambda event, arg=name: self.left_click(event, arg))
                self.dict_of_buttons[name][0].bind('<Button-3>', lambda event, arg=name: self.right_click(event, arg))
                neighbours = list()
        pp = pprint.PrettyPrinter()
        pp.pprint(self.matrix)
        return self.matrix

    def left_click(self, event, arg):
        self.time_p.configure(fg="white")
        if self.dict_of_buttons[arg][0] not in self.mark_buttons:
            if self.dict_of_buttons[arg][1] != "mine":
                if self.dict_of_buttons[arg][3] % 2 == 0:
                    self.dict_of_buttons[arg][0].configure(bg="white", text=self.dict_of_buttons[arg][1], fg=self.colour_dict[int(self.dict_of_buttons[arg][1])], relief="flat",state="disable", disabledforeground=self.colour_dict[int(self.dict_of_buttons[arg][1])])
                else:
                    self.dict_of_buttons[arg][0].configure(bg="gainsboro", text=self.dict_of_buttons[arg][1], fg="gainsboro", relief="flat",state="disable", disabledforeground=self.colour_dict[int(self.dict_of_buttons[arg][1])])
                if self.dict_of_buttons[arg][0] not in self.open_buttons:
                    self.open_buttons.append(self.dict_of_buttons[arg][0])
                if self.dict_of_buttons[arg][1] == "0":
                    self.dict_of_buttons[arg][0].configure(text="")
                    self.big_open(self.dict_of_buttons[arg][2])

            else:
                self.dict_of_buttons[arg][0].configure(fg="white", bg="red", text="M")
                self.open_buttons.append(self.dict_of_buttons[arg][0])
                self.time_p.configure(fg="blue")
                self.end_screen(self.dict_of_buttons[arg][0])
                answer = messagebox.askretrycancel("Mine! :(", "Better luck next time :P")
                if answer:
                    self.reset()
                    self.create_matrix(self.choosen.get())
                    self.marked.configure(text="Marked: " + str(self.size[self.choosen.get()][2]-len(self.mark_buttons)))
                    self.time_p.configure(fg="white")
                else:
                    exit()
            self.check_win()

    def right_click(self, event, arg):
        if self.dict_of_buttons[arg][0] not in self.open_buttons and self.dict_of_buttons[arg][0] not in self.mark_buttons:
            if len(self.mark_buttons) < self.size[self.choosen.get()][2]:
                self.dict_of_buttons[arg][0].configure(fg="green", bg="green")
                self.mark_buttons.append(self.dict_of_buttons[arg][0])
            else:
                answer = messagebox.showinfo("Warning!", "Too many marked fields!")

        elif self.dict_of_buttons[arg][0] in self.mark_buttons:
            self.dict_of_buttons[arg][0].configure(fg="gray", bg="gray")
            self.mark_buttons.remove(self.dict_of_buttons[arg][0])

        self.marked.configure(text="Marked: " + str(self.size[self.choosen.get()][2]-len(self.mark_buttons)))
        self.check_win()

    def big_open(self, lst):
        for neighbour in lst:
            if neighbour in self.dict_of_buttons:
                if self.dict_of_buttons[neighbour][1] == "0" and self.dict_of_buttons[neighbour][0] not in self.open_buttons:
                    self.open_buttons.append(self.dict_of_buttons[neighbour][0])
                    if self.dict_of_buttons[neighbour][3] % 2 == 0:
                        self.dict_of_buttons[neighbour][0].configure(bg="white", text="", relief="flat")
                    else:
                        self.dict_of_buttons[neighbour][0].configure(bg="gainsboro", text="", relief="flat")

                    self.big_open(self.dict_of_buttons[neighbour][2])
                elif self.dict_of_buttons[neighbour][0] not in self.open_buttons and self.dict_of_buttons[neighbour][1] != "mine":
                    self.open_buttons.append(self.dict_of_buttons[neighbour][0])

                    if self.dict_of_buttons[neighbour][3] % 2 == 0:
                        self.dict_of_buttons[neighbour][0].configure(bg="white", text=self.dict_of_buttons[neighbour][1], relief="flat",
                        fg=self.colour_dict[int(self.dict_of_buttons[neighbour][1])], disabledforeground=self.colour_dict[int(self.dict_of_buttons[neighbour][1])])
                    else:
                        self.dict_of_buttons[neighbour][0].configure(bg="gainsboro", text=self.dict_of_buttons[neighbour][1], relief="flat",
                        fg=self.colour_dict[int(self.dict_of_buttons[neighbour][1])], disabledforeground=self.colour_dict[int(self.dict_of_buttons[neighbour][1])])

    def check_win(self):
        print(len(self.open_buttons) + len(self.mark_buttons))
        if len(self.open_buttons) + len(self.mark_buttons) == len(self.matrix) * len(self.matrix[0]):
            self.time_p.configure(fg="blue")
            answer = messagebox.showinfo("Congratulations ;)", "Time: " + str(round(time.time()-self.start)))
            if answer:
                self.reset()
                self.create_matrix(self.choosen.get())
                self.marked.configure(text="Marked: " + str(self.size[self.choosen.get()][2]-len(self.mark_buttons)))
                self.time_p.configure(fg="white")

    def end_screen(self, stepped_on):
        for buttns in self.dict_of_buttons:
            if self.dict_of_buttons[buttns][1] == "mine" and self.dict_of_buttons[buttns][0] != stepped_on and self.dict_of_buttons[buttns][0] not in self.mark_buttons:
                self.dict_of_buttons[buttns][0].configure(bg="orange", text="M", fg="white")
            elif self.dict_of_buttons[buttns][1] != "mine" and self.dict_of_buttons[buttns][0] in self.mark_buttons and self.dict_of_buttons[buttns][0] != stepped_on:
                self.dict_of_buttons[buttns][0].configure(fg="red", text="X", bg="green2")

    def reset(self):
        self.dict_of_buttons = dict()
        self.mark_buttons = list()
        self.open_buttons = list()
        self.start = time.time()
        for widget in self.frame.winfo_children():
            widget.destroy()

    def clock(self):
        t=time.time()
        if t!='':
            self.time_p.config(text="Time: "+ str(round(t-self.start)))
        self.root.after(100, self.clock)

    def callback(self, *args):
        print(self.choosen.get())
        size_m = self.choosen.get()
        if size_m == "Easy":
            self.reset()
            self.marked.configure(text="Marked: " + str(self.size[self.choosen.get()][2]-len(self.mark_buttons)))
            self.create_matrix("Easy")
        elif size_m =="Medium":
            self.reset()
            self.marked.configure(text="Marked: " + str(self.size[self.choosen.get()][2]-len(self.mark_buttons)))
            self.create_matrix("Medium")
        else:
            self.reset()
            self.marked.configure(text="Marked: " + str(self.size[self.choosen.get()][2]-len(self.mark_buttons)))
            self.create_matrix("Hard")

    def close(self):
        self.root.mainloop()

Minesweeper()
