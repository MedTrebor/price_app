from window import Window
from create_window import CreateNewWindow
from tkinter import *


class MainWindow(Window):
    def __init__(self, window, *args):
        super().__init__(window)

        self.search_frame = LabelFrame(window)
        self.search_frame.grid(row=self.main_row, column=0, pady=5)
        self.search_label = Label(self.search_frame, text='Search:')
        self.search_label.grid(row=0, column=0)
        self.search_entry = Entry(self.search_frame, width=19)
        self.search_entry.grid(row=0, column=1)
        self.search_button = Button(self.search_frame, text='SEARCH')
        self.search_button.grid(row=0, column=2)

        self.create_new_button = Button(window, text='Create New', command=self.create_new_func)
        self.create_new_button.grid(row=self.main_row, column=0, padx=30, pady=5)


    def create_new_func(self):
        return CreateNewWindow(self.window, MainWindow)
