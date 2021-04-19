from tkinter import *
from tkinter import messagebox
from datetime import date
from database import create_in_db, search_db


class Window:
    def __init__(self, window, previous_window):
        self.window = window
        self.previous_window = previous_window
        self.main_row_count = -1
        for wgt in window.grid_slaves():
            wgt.destroy()

    @property
    def main_row(self):
        self.main_row_count += 1
        return self.main_row_count

    @property
    def main_row_same(self):
        if self.main_row_count == -1:
            self.main_row_count += 1
            return self.main_row_same
        return self.main_row_count


class MainWindow(Window):
    def __init__(self, window, previous_window, *args):
        super().__init__(window, previous_window)

        self.search_frame = LabelFrame(window)
        self.search_frame.grid(row=self.main_row, column=0, pady=5)
        self.search_label = Label(self.search_frame, text='Search:')
        self.search_label.grid(row=0, column=0)
        self.search_entry = Entry(self.search_frame, width=19)
        self.search_entry.focus_set()
        self.search_entry.bind('<Return>', self.search)
        self.search_entry.grid(row=0, column=1)
        self.search_button = Button(
            self.search_frame, text='SEARCH', command=self.search)
        self.search_button.grid(row=0, column=2)

        self.create_new_button = Button(
            window, text='Create New', command=self.create_new_func)
        self.create_new_button.grid(
            row=self.main_row, column=0, padx=30, pady=5)

    def create_new_func(self):
        return CreateNewWindow(self.window, MainWindow)

    def search(self, *args):
        return SearchWindow(self.window, MainWindow, search_db(self.search_entry.get()))


class CreateNewWindow(Window):
    def __init__(self, window, previous_window):
        super().__init__(window, previous_window)

        # PRODUCT NAME
        # product name frame
        self.product_name_frame = LabelFrame(window)
        self.product_name_frame.grid(
            row=self.main_row, column=0, columnspan=2, pady=5)

        # product name label
        self.product_name_label = Label(
            self.product_name_frame, text='Product name:')
        self.product_name_label.grid(row=0, column=0)

        # product name entry
        self.product_name_entry = Entry(self.product_name_frame, width=23)
        self.product_name_entry.grid(row=0, column=1)

        # PRODUCT TYPE
        # product type frame
        self.product_type_frame = LabelFrame(window)
        self.product_type_frame.grid(
            row=self.main_row, column=0, columnspan=2, pady=5)

        # product type label
        self.product_type_label = Label(
            self.product_type_frame, text='Product type:')
        self.product_type_label.grid(row=0, column=0)

        # product type entry
        self.product_type_entry = Entry(self.product_type_frame, width=24)
        self.product_type_entry.grid(row=0, column=1)

        # PRICE
        # price frame
        self.price_frame = LabelFrame(window)
        self.price_frame.grid(row=self.main_row, column=0,
                              columnspan=2, pady=5)

        # price label
        self.price_label = Label(self.price_frame, text='Price:')
        self.price_label.grid(row=0, column=0)

        # price entry
        self.price_entry = Entry(self.price_frame, width=30)
        self.price_entry.grid(row=0, column=1)

        # CURRENCY AND UNIT
        # currency and unit frame
        self.currency_unit_frame = LabelFrame(window)
        self.currency_unit_frame.grid(
            row=self.main_row, column=0, columnspan=2, pady=5)

        # currency label
        self.currency_label = Label(self.currency_unit_frame, text='Currency:')
        self.currency_label.grid(row=0, column=0)

        # currency entry
        self.currency_entry = Entry(self.currency_unit_frame, width=8)
        self.currency_entry.grid(row=0, column=1)
        self.currency_entry.insert(0, 'RSD')

        # unit label
        self.unit_label = Label(self.currency_unit_frame, text='Unit:')
        self.unit_label.grid(row=0, column=2)

        # unit entry
        self.unit_entry = Entry(self.currency_unit_frame, width=14)
        self.unit_entry.grid(row=0, column=3)

        # LOCATION
        # location frame
        self.location_frame = LabelFrame(window)
        self.location_frame.grid(
            row=self.main_row, column=0, columnspan=2, pady=5)

        # location name label
        self.location_name_label = Label(
            self.location_frame, text='Location name:')
        self.location_name_label.grid(row=0, column=0)

        # location name entry
        self.location_name_entry = Entry(self.location_frame, width=22)
        self.location_name_entry.grid(row=0, column=1)

        # general location frame
        self.general_location_frame = LabelFrame(window)
        self.general_location_frame.grid(
            row=self.main_row, column=0, columnspan=2, pady=5)

        # general location label
        self.general_location_label = Label(
            self.general_location_frame, text='General location:')
        self.general_location_label.grid(row=0, column=2)

        # general location entry
        self.general_location_entry = Entry(
            self.general_location_frame, width=21)
        self.general_location_entry.grid(row=0, column=3)

        # DATE
        # date frame
        self.date_frame = LabelFrame(window)
        self.date_frame.grid(row=self.main_row, column=0, columnspan=2, pady=5)

        # date label
        self.location_name_label = Label(self.date_frame, text='Date:')
        self.location_name_label.grid(row=0, column=0)

        # date entry
        self.date_today = date.today()
        # day entry
        self.day_entry = Entry(self.date_frame, width=3)
        self.day_entry.grid(row=0, column=1)
        self.day_entry.insert(0, str(self.date_today)[8:])
        # month entry
        self.month_entry = Entry(self.date_frame, width=3)
        self.month_entry.grid(row=0, column=2)
        self.month_entry.insert(0, str(self.date_today)[5:7])
        # year entry
        self.year_entry = Entry(self.date_frame, width=5)
        self.year_entry.grid(row=0, column=3)
        self.year_entry.insert(0, str(self.date_today)[:4])

        # CITY
        # city frame
        self.city_frame = LabelFrame(window)
        self.city_frame.grid(row=self.main_row, column=0, columnspan=2, pady=5)
        # city label
        self.city_label = Label(self.city_frame, text='City:')
        self.city_label.grid(row=0, column=4)

        # city entry
        self.city_entry = Entry(self.city_frame, width=31)
        self.city_entry.grid(row=0, column=5)
        self.city_entry.insert(0, 'Novi Sad')

        # CANCEL BUTTON
        self.cancel_button = Button(window, text='CANCEL', command=self.cancel)
        self.cancel_button.grid(row=self.main_row, column=0, pady=5)

        # CREATE BUTTON
        self.create_execute_button = Button(
            window, text='CREATE', command=self.create_execute)
        self.create_execute_button.grid(
            row=self.main_row_same, column=1, pady=5)

        # # # SIZE REFERENCE # # #
        self.lbl = Label(window, text='020406081012141618202224262830323436')
        self.lbl.grid(row=self.main_row, column=0, columnspan=2)
        self.et = Entry(window, width=36)
        self.et.grid(row=self.main_row, column=0, columnspan=2)

    def cancel(self):
        return self.previous_window(self.window, self.previous_window)

    def create_execute(self):
        # initiating validation
        if self.validate():

            # creating full date
            submit_date = self.year_entry.get() + '-' + self.month_entry.get() + \
                '-' + self.day_entry.get()

            # submitting to database
            return create_in_db(
                product_type=self.product_type_entry.get(),
                product_name=self.product_name_entry.get(),
                location_name=self.location_name_entry.get(),
                city=self.city_entry.get(),
                general_location=self.general_location_entry.get(),
                price=self.price_entry.get(),
                currency=self.currency_entry.get(),
                unit=self.unit_entry.get(),
                date=submit_date
            )  # , CreateNewWindow(self.window, self.previous_window)

    def validate(self):
        # validating field length
        if len(self.product_name_entry.get()) == 0:
            return self.warning()
        elif len(self.product_type_entry.get()) == 0:
            return self.warning()
        elif len(self.price_entry.get()) == 0 or len(self.price_entry.get()) > 9:
            return self.warning()
        elif len(self.currency_entry.get()) == 0:
            return self.warning()
        elif len(self.unit_entry.get()) == 0:
            return self.warning()
        elif len(self.location_name_entry.get()) == 0:
            return self.warning()
        elif len(self.general_location_entry.get()) == 0:
            return self.warning()
        elif len(self.day_entry.get()) == 0 or len(self.day_entry.get()) > 2:
            return self.warning()
        elif len(self.month_entry.get()) == 0 or len(self.day_entry.get()) > 2:
            return self.warning()
        elif len(self.month_entry.get()) == 0 or len(self.day_entry.get()) > 4:
            return self.warning()
        elif len(self.city_entry.get()) == 0:
            return self.warning()

        # validating numbers
        try:
            float(self.price_entry.get())
            if int(self.day_entry.get()) > 31 or int(self.month_entry.get()) > 12:
                return self.warning()
        except ValueError:
            return self.warning()
        return True

    # producing warning message
    @staticmethod
    def warning():
        return messagebox.showwarning('Warning', 'Entered fields are not valid')


class SearchWindow(Window):
    def __init__(self, window, previous_window, query, *args):
        super().__init__(window, previous_window)
        self.query = query

        # search bar
        self.search_frame = LabelFrame(window)
        self.search_frame.grid(
            row=self.main_row, column=0, pady=5, columnspan=2)
        self.search_label = Label(self.search_frame, text='Search:')
        self.search_label.grid(row=0, column=0)
        self.search_entry = Entry(self.search_frame, width=21)
        self.search_entry.grid(row=0, column=1)
        self.search_entry.focus_set()
        self.search_entry.bind('<Return>', self.search)
        self.search_entry.insert(0, self.query[0][1])
        self.search_button = Button(
            self.search_frame, text='SEARCH', command=self.search)
        self.search_button.grid(row=0, column=2)

        # canvas
        self.canvas = Canvas(self.window, width=290, height=500)
        self.canvas_frame = Frame(self.canvas)
        self.scroll_bar = Scrollbar(
            self.window, orient='vertical', command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.grid(row=self.main_row, column=0)
        self.scroll_bar.grid(row=self.main_row_same, column=1, sticky=N+S)

        self.canvas.create_window((0, 0), window=self.canvas_frame)
        self.canvas_frame.bind('<Configure>', self.scroll_region)

        # search content
        self.populate()

        # setting scroll
        self.window.bind_all('<Button-4>', self.mouse_scroll)
        self.window.bind_all('<Button-5>', self.mouse_scroll)

        # create button
        self.create_new_button = Button(
            window, text='Create New', command=self.create_new_func)
        self.create_new_button.grid(
            row=self.main_row, column=0, padx=30, pady=5, columnspan=2)

        # # # SIZE REFERENCE # # #
        self.lbl = Label(window, text='02040608101214161820222426283032343637')
        self.lbl.grid(row=self.main_row, column=0, columnspan=2)
        self.et = Entry(window, width=38)
        self.et.grid(row=self.main_row, column=0, columnspan=2)

    def create_new_func(self):
        return CreateNewWindow(self.window, MainWindow)

    # open DetailWindow
    def open_details(self, item, query):
        saving_item = item
        saving_query = query
        window = self.window

        def inner():
            return DetailWindow(window, SearchWindow, saving_item, saving_query)
        return inner

    def search(self, *args):
        return SearchWindow(self.window, MainWindow, search_db(self.search_entry.get()))

    # SEARCHED CONTENT
    def populate(self):
        count = 1
        row_count = 0
        item_count = 0
        for item in self.query:
            Label(self.canvas_frame, text=f'{count}.').grid(
                row=row_count, column=0, rowspan=3)
            Label(self.canvas_frame, text=item[0]).grid(
                row=row_count, column=1, pady=5)
            Label(self.canvas_frame, text=f'{item[2]} {item[3]}').grid(
                row=row_count, column=2, pady=5)
            row_count += 1

            Label(self.canvas_frame, text=item[5]).grid(
                row=row_count, column=1)
            Label(self.canvas_frame, text=item[7]).grid(
                row=row_count, column=2, pady=5)
            row_count += 1

            Label(self.canvas_frame, text=item[6]).grid(
                row=row_count, column=1)
            Button(self.canvas_frame, text='details', command=self.open_details(
                item_count, self.query)).grid(row=row_count, column=2)
            row_count += 1

            Label(self.canvas_frame, text='-' *
                  57).grid(row=row_count, columnspan=3)
            row_count += 1

            count += 1
            item_count += 1

    # scroll region
    def scroll_region(self, *args):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    # mouse scroll
    def mouse_scroll(self, event):
        direction = 0
        if event.num == 5 or event.delta == -120:
            direction = 1
        elif event.num == 4 or event.delta == 120:
            direction = -1
        self.canvas.yview_scroll(direction, UNITS)


class DetailWindow(Window):
    def __init__(self, window, previous_window, item_no, query):
        super().__init__(window, previous_window)
        self.item_no = item_no
        self.item = query[item_no]
        self.query = query

        # PRODUCT NAME
        # product name frame
        self.product_name_frame = LabelFrame(window)
        self.product_name_frame.grid(row=self.main_row, column=0, columnspan=3)

        # product name label
        self.product_name_label = Label(
            self.product_name_frame, text='Product name:', width=15, anchor=W)
        self.product_name_label.grid(row=0, column=0)

        # product name item label
        self.product_name_item_label = Label(
            self.product_name_frame, text=self.item[0], width=22, anchor=CENTER)
        self.product_name_item_label.grid(row=0, column=1)

        # PRODUCT TYPE
        # product type frame
        self.product_type_frame = LabelFrame(window)
        self.product_type_frame.grid(row=self.main_row, column=0, columnspan=3)

        # product type label
        self.product_type_label = Label(
            self.product_type_frame, text='Product type:', width=15, anchor=W)
        self.product_type_label.grid(row=0, column=0)

        # product type item label
        self.product_type_item_label = Label(
            self.product_type_frame, text=self.item[1], width=22, anchor=CENTER)
        self.product_type_item_label.grid(row=0, column=1)

        # PRICE
        # price frame
        self.price_frame = LabelFrame(self.window)
        self.price_frame.grid(row=self.main_row, column=0, columnspan=3)

        # price label
        self.price_label = Label(
            self.price_frame, text='Price:', width=15, anchor=W)
        self.price_label.grid(row=0, column=0)

        # price item label
        self.price_item_label = Label(
            self.price_frame, text=f'{self.item[2]} {self.item[3]}/{self.item[4]}',
            width=22, anchor=CENTER)
        self.price_item_label.grid(row=0, column=1)

        # LOCATION NAME
        # location name frame
        self.location_name_frame = LabelFrame(self.window)
        self.location_name_frame.grid(
            row=self.main_row, column=0, columnspan=3)

        # location name label
        self.location_name_label = Label(
            self.location_name_frame, text='Location name:', width=15, anchor=W)
        self.location_name_label.grid(row=0, column=0)

        # location name item label
        self.location_name_item_label = Label(
            self.location_name_frame, text=self.item[5], width=22, anchor=CENTER)
        self.location_name_item_label.grid(row=0, column=1)

        # GENERAL LOCATION
        # general_location frame
        self.general_location_frame = LabelFrame(self.window)
        self.general_location_frame.grid(
            row=self.main_row, column=0, columnspan=3)

        # general_location label
        self.general_location_label = Label(
            self.general_location_frame, text='General location:', width=15, anchor=W)
        self.general_location_label.grid(row=0, column=0)

        # general_location item label
        self.general_location_item_label = Label(
            self.general_location_frame, text=self.item[6], width=22, anchor=CENTER)
        self.general_location_item_label.grid(row=0, column=1)

        # DATE
        # date frame
        self.date_frame = LabelFrame(self.window)
        self.date_frame.grid(
            row=self.main_row, column=0, columnspan=3)

        # date label
        self.date_label = Label(
            self.date_frame, text='Date:', width=15, anchor=W)
        self.date_label.grid(row=0, column=0)

        # date item label
        self.date_item_label = Label(
            self.date_frame, text=self.item[7], width=22, anchor=CENTER)
        self.date_item_label.grid(row=0, column=1)

        # CITY
        # city frame
        self.city_frame = LabelFrame(self.window)
        self.city_frame.grid(
            row=self.main_row, column=0, columnspan=3)

        # city label
        self.city_label = Label(
            self.city_frame, text='City:', width=15, anchor=W)
        self.city_label.grid(row=0, column=0)

        # city item label
        self.city_item_label = Label(
            self.city_frame, text=self.item[8], width=22, anchor=CENTER)
        self.city_item_label.grid(row=0, column=1)

        # # # PREVIOUS AND NEXT BUTTONS
        # PREVIUOUS BUTTON
        self.set_previous_button()

        # NEXT BUTTON
        self.set_next_button()

        # BACK BUTTON
        self.back_button = Button(window, text='BACK', command=self.back)
        self.back_button.grid(row=self.main_row_same, column=1,
                              pady=5)

        # # # SIZE REFERENCE # # #
        self.lbl = Label(window, text='0204060810121416182022242628303234367')
        self.lbl.grid(row=self.main_row, column=0, columnspan=3)
        self.et = Entry(window, width=38)
        self.et.grid(row=self.main_row, column=0, columnspan=3)

    def back(self):
        return self.previous_window(self.window, self.previous_window, self.query)

    def set_previous_button(self):
        if self.item_no == 0:
            previous_button = Button(self.window, text='<<', state=DISABLED)
            previous_button.grid(row=self.main_row, column=0)
        else:
            previous_button = Button(
                self.window, text='<<', command=self.previous)
            previous_button.grid(row=self.main_row, column=0)

    def set_next_button(self):
        if self.item_no + 1 == len(self.query):
            next_button = Button(self.window, text='>>', state=DISABLED)
            next_button.grid(row=self.main_row_same, column=2)
        else:
            next_button = Button(self.window, text='>>',
                                 command=self.next_meth)
            next_button.grid(row=self.main_row_same, column=2)

    def previous(self):
        return DetailWindow(self.window, self.previous_window, self.item_no-1, self.query)

    def next_meth(self):
        return DetailWindow(self.window, self.previous_window, self.item_no+1, self.query)


if __name__ == '__main__':
    root = Tk()

    SearchWindow(root, MainWindow, search_db('mleko'))
    root.mainloop()

# # # MOBILE REFERENCES # # #
# Canvas(width=1000, height=1800)
# separator: 70*'-'
