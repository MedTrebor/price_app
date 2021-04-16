from tkinter import *
from tkinter import filedialog, messagebox
from datetime import date
import io
import os
from database import create_in_db, search_db
from PIL import Image as Image_pil, ImageTk as ImageTk_pil


class Window:
    def __init__(self, window, previous_window):
        self.window = window
        self.previous_window = previous_window
        self.main_row_count = 0
        for wgt in window.grid_slaves():
            wgt.destroy()

    @property
    def main_row(self):
        self.main_row_count += 1
        return self.main_row_count - 1


class MainWindow(Window):
    def __init__(self, window, previous_window, *args):
        super().__init__(window, previous_window)

        self.search_frame = LabelFrame(window)
        self.search_frame.grid(row=self.main_row, column=0, pady=5)
        self.search_label = Label(self.search_frame, text='Search:')
        self.search_label.grid(row=0, column=0)
        self.search_entry = Entry(self.search_frame, width=19)
        self.search_entry.grid(row=0, column=1)
        self.search_button = Button(self.search_frame, text='SEARCH', command=self.search)
        self.search_button.grid(row=0, column=2)

        self.create_new_button = Button(window, text='Create New', command=self.create_new_func)
        self.create_new_button.grid(row=self.main_row, column=0, padx=30, pady=5)

    def create_new_func(self):
        return CreateNewWindow(self.window, MainWindow)

    def search(self):
        return SearchWindow(self.window, MainWindow, self.search_entry.get())


class CreateNewWindow(Window):
    def __init__(self, window, previous_window):
        self.picture = io.BytesIO()
        super().__init__(window, previous_window)

        # PRODUCT NAME
        # product name frame
        self.product_name_frame = LabelFrame(window)
        self.product_name_frame.grid(row=self.main_row, column=0, columnspan=2, pady=5)

        # product name label
        self.product_name_label = Label(self.product_name_frame, text='Product name:')
        self.product_name_label.grid(row=0, column=0)

        # product name entry
        self.product_name_entry = Entry(self.product_name_frame, width=23)
        self.product_name_entry.grid(row=0, column=1)

        # PICTURE
        # picture button
        self.picture_button = Button(window, text='Upload picture', command=self.upload)
        self.picture_button.grid(row=self.main_row, column=0, columnspan=2, pady=5)
        # create upload window

        # PRODUCT TYPE
        # product type frame
        self.product_type_frame = LabelFrame(window)
        self.product_type_frame.grid(row=self.main_row, column=0, columnspan=2, pady=5)

        # product type label
        self.product_type_label = Label(self.product_type_frame, text='Product type:')
        self.product_type_label.grid(row=0, column=0)

        # product type entry
        self.product_type_entry = Entry(self.product_type_frame, width=24)
        self.product_type_entry.grid(row=0, column=1)

        # PRICE AND UNIT
        # price and unit frame
        self.price_and_unit_frame = LabelFrame(window)
        self.price_and_unit_frame.grid(row=self.main_row, column=0, columnspan=2, pady=5)

        # price label
        self.price_label = Label(self.price_and_unit_frame, text='Price:')
        self.price_label.grid(row=0, column=0)

        # price entry
        self.price_entry = Entry(self.price_and_unit_frame, width=15)
        self.price_entry.grid(row=0, column=1)

        # unit label
        self.unit_label = Label(self.price_and_unit_frame, text='Unit:')
        self.unit_label.grid(row=0, column=2)

        # unit entry
        self.unit_entry = Entry(self.price_and_unit_frame, width=10)
        self.unit_entry.grid(row=0, column=3)

        # LOCATION
        # location frame
        self.location_frame = LabelFrame(window)
        self.location_frame.grid(row=self.main_row, column=0, columnspan=2, pady=5)

        # location name label
        self.location_name_label = Label(self.location_frame, text='Location name:')
        self.location_name_label.grid(row=0, column=0)

        # location name entry
        self.location_name_entry = Entry(self.location_frame, width=22)
        self.location_name_entry.grid(row=0, column=1)

        # general location frame
        self.general_location_frame = LabelFrame(window)
        self.general_location_frame.grid(row=self.main_row, column=0, columnspan=2, pady=5)

        # general location label
        self.general_location_label = Label(self.general_location_frame, text='General location:')
        self.general_location_label.grid(row=0, column=2)

        # general location entry
        self.general_location_entry = Entry(self.general_location_frame, width=21)
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
        self.main_row_count -= 1
        # cancel function

        # CREATE BUTTON
        self.create_execute_button = Button(window, text='CREATE', command=self.create_execute)
        self.create_execute_button.grid(row=self.main_row, column=1, pady=5)
        # create execute function

        # # # SIZE REFERENCE # # #
        self.lbl = Label(window, text='020406081012141618202224262830323436')
        self.lbl.grid(row=self.main_row, column=0, columnspan=2)
        self.et = Entry(window, width=36)
        self.et.grid(row=self.main_row, column=0, columnspan=2)
        self.fr = LabelFrame(window)
        self.fr.grid(row=self.main_row, column=0, columnspan=2)
        self.et_fr = Entry(self.fr, width=36)
        self.et_fr.grid(row=0, column=0)

    def cancel(self):
        return self.previous_window(self.window, self.previous_window)

    def upload(self):
        # opening file browser
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title='Select image',
            filetypes=(
                ('all files', '*.*'),
                ('jpg image', '*.jpg'),
                ('jpeg image', '*.jpeg'),
                ('png image', '*.png')
            )
        )
        try:
            # opening and cropping image
            img = Image_pil.open(filename)
            cropped_img = img.crop((0, 0, min(img.size), min(img.size)))
            cropped_img.thumbnail((300, 300))

            # converting to bytes
            self.picture = io.BytesIO()
            cropped_img.save(self.picture, format='PNG')
        except AttributeError:
            pass

    def create_execute(self):
        # initiating validation
        if self.validate():

            # creating full date
            submit_date = self.year_entry.get() + '-' + self.month_entry.get() + '-' + self.day_entry.get()

            # submitting to database with no picture
            if len(self.picture.getvalue()) == 0:
                return create_in_db(
                    product_type=self.product_type_entry.get(),
                    product_name=self.product_name_entry.get(),
                    location_name=self.location_name_entry.get(),
                    city=self.city_entry.get(),
                    general_location=self.general_location_entry.get(),
                    price=self.price_entry.get(),
                    unit=self.unit_entry.get(),
                    date=submit_date
                )#, CreateNewWindow(self.window, self.previous_window)

            # submitting to database with picture
            else:
                return create_in_db(
                    product_type=self.product_type_entry.get(),
                    product_name=self.product_name_entry.get(),
                    picture=self.picture,
                    location_name=self.location_name_entry.get(),
                    city=self.city_entry.get(),
                    general_location=self.general_location_entry.get(),
                    price=self.price_entry.get(),
                    unit=self.unit_entry.get(),
                    date=submit_date
                )#, CreateNewWindow(self.window, self.previous_window)

    def validate(self):
        # validating field length
        if len(self.product_name_entry.get()) == 0:
            return self.warning()
        elif len(self.product_type_entry.get()) == 0:
            return self.warning()
        elif len(self.price_entry.get()) == 0 or len(self.price_entry.get()) > 9:
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

        self.search_frame = LabelFrame(window)
        self.search_frame.grid(row=self.main_row, column=0, pady=5, columnspan=4)
        self.search_label = Label(self.search_frame, text='Search:')
        self.search_label.grid(row=0, column=0)
        self.search_entry = Entry(self.search_frame, width=19)
        self.search_entry.grid(row=0, column=1)
        self.search_button = Button(self.search_frame, text='SEARCH')
        self.search_button.grid(row=0, column=2)

        # iterating through db_query
        self.count = 1
        for item in search_db(self.query):
            self.row_1 = self.main_row
            self.row_2 = self.main_row
            Label(window, text=f'{self.count}').grid(row=self.row_1, column=0, rowspan=2)
            Label(window, text=item[0]).grid(row=self.row_1, column=1, pady=5, padx=2)
            Label(window, text=f'{item[3]} din.').grid(row=self.row_1, column=2, pady=5, padx=2)
            Label(window, text=f'{item[5]} - {item[6]}').grid(row=self.row_2, column=1, padx=2, columnspan=2)
            Button(window, text='details', command=self.open_details(item)).grid(row=self.row_1, rowspan=2, column=3, padx=2)
            Label(window, text='-'*55).grid(row=self.main_row, columnspan=4)
            self.count += 1

        # setting up buttons
        self.create_new_button = Button(window, text='Create New', command=self.create_new_func)
        self.create_new_button.grid(row=self.main_row, column=0, padx=30, pady=5, columnspan=4)

    def create_new_func(self):
        return CreateNewWindow(self.window, MainWindow)

    # create button for details
    def open_details(self, item):
        saving_item = item
        window = self.window

        def inner():
            return DetailWindow(window, CreateNewWindow, saving_item)
        return inner



class DetailWindow(Window):
    def __init__(self, window, previous_window, item):
        super().__init__(window, previous_window)
        self.item = search_db('mleko')

        if self.item[1] is not None:
            # product name
            self.product_name_label = Label(window, text=item[0])
            self.product_name_label.grid(row=self.main_row, column=0, columnspan=4)

            # picture
            self.img = Image_pil.open(io.BytesIO(self.item[0][1]))
            self.picture = ImageTk_pil.PhotoImage(self.img)
            self.picture_label = Label(window, image=self.picture)
            self.picture_label.grid(row=self.main_row, column=0, columnspan=4)
            # # # CAN'T PRODUCE PICTURE # # #

            # product type
            self.product_type_label = Label(window, text=item[2])
            self.product_type_label.grid(row=self.main_row, column=0, columnspan=4)


