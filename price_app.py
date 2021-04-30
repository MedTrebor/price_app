from tkinter import *
from tkinter import messagebox, filedialog
from datetime import date
from PIL import Image as ImagePIL, ImageTk, UnidentifiedImageError
import io
import os
from database import (
    create_in_db,
    search_db,
    update_price_db,
    update_product_db,
    update_location_db,
    delete_db
)


# # # WINDOW PARENT # # #
class Window:
    def __init__(self, window, previous_window):
        self.window = window
        self.previous_window = previous_window
        self.main_row_count = -1
        for wgt in window.grid_slaves():
            wgt.destroy()

        # unbinding
        self.window.unbind('<Button-4>')
        self.window.unbind('<Button-5>')
        self.window.unbind('<Return>')
        self.window.unbind('<Escape>')
        self.window.unbind('<Left>')
        self.window.unbind('<Right>')

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


# # # MAIN WINDOW # # #
class MainWindow(Window):
    def __init__(self, window, previous_window, *args):
        super().__init__(window, previous_window)

        self.search_frame = LabelFrame(window)
        self.search_frame.grid(row=self.main_row, column=0, pady=5)
        self.search_label = Label(self.search_frame, text='Search:')
        self.search_label.grid(row=0, column=0)
        self.search_entry = Entry(self.search_frame, width=22)
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
        search_phrase = self.search_entry.get()
        query = search_db(search_phrase)
        if query != []:
            return SearchWindow(self.window, MainWindow, query, search_phrase)
        else:
            return MainWindow(self.window, MainWindow)


# # # CREATE WINDOW # # #
class CreateNewWindow(Window):
    def __init__(self, window, previous_window, **kwargs):
        super().__init__(window, previous_window)
        self.query = kwargs.get('query')
        self.search_phrase = kwargs.get('search_phrase', 'qwerty')
        self.product = kwargs.get('product', None)
        self.keep_location = kwargs.get('keep_location', None)
        self.picture = io.BytesIO()

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
        self.product_name_entry = Entry(self.product_name_frame, width=26)
        self.product_name_entry.grid(row=0, column=1)
        self.product_name_entry.focus_set()

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
        self.product_type_entry = Entry(self.product_type_frame, width=27)
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
        self.price_entry = Entry(self.price_frame, width=33)
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
        self.currency_entry = Entry(self.currency_unit_frame, width=6)
        self.currency_entry.grid(row=0, column=1)
        self.currency_entry.insert(0, 'RSD')

        # unit label
        self.unit_label = Label(self.currency_unit_frame, text='Unit:')
        self.unit_label.grid(row=0, column=2)

        # unit number
        self.unit_number = Entry(self.currency_unit_frame, width=6)
        self.unit_number.grid(row=0, column=3)
        self.unit_number.insert(0, '1')

        # unit entry
        self.unit_entry = Entry(self.currency_unit_frame, width=12)
        self.unit_entry.grid(row=0, column=4)

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
        self.location_name_entry = Entry(self.location_frame, width=25)
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
            self.general_location_frame, width=24)
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
        self.city_entry = Entry(self.city_frame, width=34)
        self.city_entry.grid(row=0, column=5)
        self.city_entry.insert(0, 'Novi Sad')

        # KEEP LOCATION CHECKBOX
        self.keep_location_var = IntVar()
        self.keep_location_var.set(0)
        self.keep_location_check = Checkbutton(
            self.window, text='KEEP LOCATION', variable=self.keep_location_var)
        self.keep_location_check.grid(
            row=self.main_row, column=0, columnspan=2, sticky=W)

        # UPLOAD BUTTON
        self.upload_button = Button(
            self.window, text='UPLOAD PICTURE', command=self.upload)
        self.upload_button.grid(
            row=self.main_row, column=0, columnspan=2, pady=5)

        # CANCEL BUTTON
        self.cancel_button = Button(window, text='CANCEL', command=self.cancel)
        self.cancel_button.grid(row=self.main_row, column=0, pady=5)

        # CREATE BUTTON
        self.create_execute_button = Button(
            window, text='CREATE', command=self.create_execute)
        self.create_execute_button.grid(
            row=self.main_row_same, column=1, pady=5)

        # bind <Return> and <Escape>
        self.window.bind('<Return>', self.create_execute)
        self.window.bind('<Escape>', self.cancel)

        # ADDING MORE PRICES FOR SAME PRODUCT
        if self.product is not None:
            self.product_name_entry.insert(0, self.product[0])
            self.product_name_entry.configure(state=DISABLED)
            self.product_type_entry.insert(0, self.product[1])
            self.product_type_entry.configure(state=DISABLED)
            self.currency_entry.delete(0, END)
            self.currency_entry.insert(0, self.product[2])
            self.unit_number.delete(0, END)
            self.unit_number.insert(0, self.product[3])
            self.unit_entry.insert(0, self.product[4])
            self.upload_button.configure(state=DISABLED)

        # KEEPING LOCATION DATA
        if self.keep_location is not None:
            self.location_name_entry.insert(0, self.keep_location[0])
            self.general_location_entry.insert(0, self.keep_location[1])

            self.day_entry.delete(0, END)
            self.month_entry.delete(0, END)
            self.year_entry.delete(0, END)
            self.city_entry.delete(0, END)

            self.day_entry.insert(0, self.keep_location[2])
            self.month_entry.insert(0, self.keep_location[3])
            self.year_entry.insert(0, self.keep_location[4])
            self.city_entry.insert(0, self.keep_location[5])
            self.keep_location_check.select()

    # UPLOAD PICTURE
    def upload(self):
        # opening file browser
        filename = filedialog.askopenfilename(
            # initialdir=os.getcwd(),
            initialdir='/home/medtrebor/Desktop/temp',
            title='Select picture',
            filetypes=(('all files', '*.*'),)
        )
        try:
            img = ImagePIL.open(filename)
        except UnidentifiedImageError:
            messagebox.showerror('Error', 'Unsupported image!')
        except AttributeError:
            pass
        else:
            # converting to RGB
            if img.mode != 'RGB':
                img.convert('RGB')

            # cropping image
            if img.size[0] > img.size[1]:
                x = (img.size[0] - img.size[1]) // 2
                cropped_img = img.crop((x, 0, img.size[0]-x, img.size[1]))
            elif img.size[0] < img.size[1]:
                x = (img.size[1] - img.size[0]) // 2
                cropped_img = img.crop((0, x, img.size[0], img.size[1]-x))
            else:
                cropped_img = img

            # resizing image
            cropped_img.thumbnail((1000, 1000))

            # converting to bytes
            self.picture = io.BytesIO()
            cropped_img.save(self.picture, format='JPEG', quality=30)

    # CANCEL

    def cancel(self, *args):
        query = search_db(self.search_phrase)
        if query == []:
            return MainWindow(self.window, MainWindow)
        else:
            return self.previous_window(self.window, self.previous_window, query, self.search_phrase)

    # CREATE ITEM
    def create_execute(self, *args):
        # initiating validation
        if self.validate() is True:

            # creating full date
            submit_date = self.year_entry.get() + '-' + self.month_entry.get() + \
                '-' + self.day_entry.get()

            # creating price_per_unit
            price_per_unit = float(self.price_entry.get()) * \
                1 / float(self.unit_number.get())

            # inserting to db with no picture
            if len(self.picture.getvalue()) == 0:
                create_in_db(
                    product_type=self.product_type_entry.get(),
                    product_name=self.product_name_entry.get(),
                    location_name=self.location_name_entry.get(),
                    city=self.city_entry.get(),
                    general_location=self.general_location_entry.get(),
                    price=self.price_entry.get(),
                    price_per_unit=str(price_per_unit),
                    currency=self.currency_entry.get(),
                    unit=self.unit_entry.get(),
                    date=submit_date
                )
            # inserting to db with picture
            else:
                create_in_db(
                    product_type=self.product_type_entry.get(),
                    product_name=self.product_name_entry.get(),
                    location_name=self.location_name_entry.get(),
                    city=self.city_entry.get(),
                    general_location=self.general_location_entry.get(),
                    price=self.price_entry.get(),
                    price_per_unit=str(price_per_unit),
                    currency=self.currency_entry.get(),
                    unit=self.unit_entry.get(),
                    date=submit_date,
                    picture=self.picture.getvalue()
                )
            query = search_db(self.search_phrase)
            if self.keep_location_var.get() == 0:
                CreateNewWindow(self.window, self.previous_window, query=query)
            else:
                keep_location = (
                    self.location_name_entry.get(),
                    self.general_location_entry.get(),
                    self.day_entry.get(),
                    self.month_entry.get(),
                    self.year_entry.get(),
                    self.city_entry.get()
                )
                CreateNewWindow(self.window, self.previous_window,
                                query=query, keep_location=keep_location)

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
        elif len(self.unit_number.get()) == 0:
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
        elif len(self.year_entry.get()) == 0 or len(self.day_entry.get()) > 4:
            return self.warning()
        elif len(self.city_entry.get()) == 0:
            return self.warning()

        # validating numbers
        try:
            float(self.price_entry.get())
            float(self.unit_number.get())
            if int(self.day_entry.get()) > 31 or int(self.day_entry.get()) < 1 or int(self.month_entry.get()) > 12 or int(self.month_entry.get()) < 1:
                return self.warning()
        except ValueError:
            return self.warning()
        return True

    # producing warning message
    @staticmethod
    def warning():
        return messagebox.showwarning('Warning', 'Entered fields are not valid')


# # # SEARCH WINDOW # # #
class SearchWindow(Window):
    def __init__(self, window, previous_window, query, search_phrase, *args):
        super().__init__(window, previous_window)
        self.query = query
        self.search_phrase = search_phrase

        # SEARCH BAR
        # search frame
        self.search_frame = LabelFrame(window)
        self.search_frame.grid(
            row=self.main_row, column=0, pady=5, columnspan=2)
        # search label
        self.search_label = Label(self.search_frame, text='Search:')
        self.search_label.grid(row=0, column=0)
        # search entry
        self.search_entry = Entry(self.search_frame, width=22)
        self.search_entry.grid(row=0, column=1)
        self.search_entry.focus_set()
        self.search_entry.bind('<Return>', self.search)
        # search button
        self.search_button = Button(
            self.search_frame, text='SEARCH', command=self.search)
        self.search_button.grid(row=0, column=2)
        # inserting query in search entry
        self.search_entry.insert(0, self.search_phrase)

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
        self.window.bind('<Button-4>', self.mouse_scroll)
        self.window.bind('<Button-5>', self.mouse_scroll)

        # create button
        self.create_new_button = Button(
            window, text='Create New', command=self.create_new_func)
        self.create_new_button.grid(
            row=self.main_row, column=0, padx=30, pady=5, columnspan=2)

    def create_new_func(self):
        return CreateNewWindow(
            self.window,
            SearchWindow,
            query=self.query,
            search_phrase=self.search_phrase
        )

    # open DetailWindow
    def open_details(self, item, query):
        saving_item = item
        saving_query = query
        window = self.window
        search_phrase = self.search_phrase

        def inner():
            return DetailWindow(window, SearchWindow, saving_item, saving_query, search_phrase)
        return inner

    # open SearchWindow
    def search(self, *args):
        search_phrase = self.search_entry.get()
        query = search_db(search_phrase)
        if query != []:
            return SearchWindow(self.window, MainWindow, query, search_phrase)
        else:
            return MainWindow(self.window, MainWindow)

    # SEARCHED CONTENT
    def populate(self):
        count = 1
        row_count = 0
        item_count = 0
        for item in self.query:
            Label(self.canvas_frame, text=f'{count}.').grid(
                row=row_count, column=0, rowspan=3)
            Label(self.canvas_frame, text=item[0], wraplength=160, justify="center").grid(
                row=row_count, column=1, pady=5)
            Label(self.canvas_frame, text=f'{item[12]:.2f} {item[3]}/{item[4]}').grid(
                row=row_count, column=2, pady=5)
            row_count += 1

            Label(self.canvas_frame, text=item[5]).grid(
                row=row_count, column=1)
            day = item[7][-2:]
            month = item[7][5:7]
            year = item[7][:4]
            Label(self.canvas_frame, text=f'{day}.{month}.{year}.').grid(
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
        self.scroll_bar.set(0, 0)

    # mouse scroll
    def mouse_scroll(self, event):
        direction = 0
        if event.num == 5 or event.delta == -120:
            direction = 1
        elif event.num == 4 or event.delta == 120:
            direction = -1
        self.canvas.yview_scroll(direction, UNITS)


# # # DETAIL WINDOW # # #
class DetailWindow(Window):
    def __init__(self, window, previous_window, item_no, query, search_phrase):
        super().__init__(window, previous_window)
        self.item_no = item_no
        self.item = query[item_no]
        self.query = query
        self.search_phrase = search_phrase

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
            self.product_name_frame, text=self.item[0], width=23, anchor=CENTER, wraplength=182, justify="center")
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
            self.product_type_frame, text=self.item[1], width=23, anchor=CENTER)
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
            self.price_frame, text=f'{self.item[2]:.2f} {self.item[3]}', width=23, anchor=CENTER)
        self.price_item_label.grid(row=0, column=1)

        # PRICE PER UNIT
        # price per unit frame
        self.price_per_unit_frame = LabelFrame(self.window)
        self.price_per_unit_frame.grid(
            row=self.main_row, column=0, columnspan=3)

        # price per unit label
        self.price_per_unit_label = Label(
            self.price_per_unit_frame, text='Price per unit:', width=15, anchor=W)
        self.price_per_unit_label.grid(row=0, column=0)

        # price per unit item label
        self.price_per_unit_item_label = Label(
            self.price_per_unit_frame, text=f'{self.item[12]:.2f} {self.item[3]}/{self.item[4]}',
            width=23, anchor=CENTER)
        self.price_per_unit_item_label.grid(row=0, column=1)

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
            self.location_name_frame, text=self.item[5], width=23, anchor=CENTER)
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
            self.general_location_frame, text=self.item[6], width=23, anchor=CENTER)
        self.general_location_item_label.grid(row=0, column=1)

        # DATE
        self.srb_date = self.item[7]
        self.day = self.srb_date[-2:]
        self.month = self.srb_date[5:7]
        self.year = self.srb_date[:4]

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
            self.date_frame, text=f'{self.day}.{self.month}.{self.year}.', width=23, anchor=CENTER)
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
            self.city_frame, text=self.item[8], width=23, anchor=CENTER)
        self.city_item_label.grid(row=0, column=1)

        # PICTURE
        self.img_canvas = Canvas(self.window, width=300, height=300)
        self.img_canvas.grid(row=self.main_row, column=0, columnspan=3)
        if self.item[11] is not None:
            self.img_from_bytes = ImagePIL.open(io.BytesIO(self.item[11]))
            self.img_from_bytes.thumbnail((300, 300))
            self.img_canvas.img = ImageTk.PhotoImage(
                self.img_from_bytes)
            self.img_canvas.create_image(
                0, 0, anchor=NW, image=self.img_canvas.img)

        # # # PREVIOUS AND NEXT BUTTONS
        # PREVIUOUS BUTTON
        self.set_previous_button()

        # NEXT BUTTON
        self.set_next_button()

        # ADD PRICE BUTTON
        self.add_price_button = Button(
            self.window, text='ADD PRICE', command=self.add_price)
        self.add_price_button.grid(row=self.main_row_same, column=1)

        # EDIT BUTTON
        self.edit_button = Button(
            self.window, text='EDIT', padx=21, command=self.edit)
        self.edit_button.grid(row=self.main_row, column=0, pady=5)

        # BACK BUTTON
        self.back_button = Button(window, text='BACK', command=self.back)
        self.back_button.grid(row=self.main_row_same, column=1,
                              pady=5)

        # DELETE BUTTON
        self.delete_button = Button(
            self.window, text='DELETE', command=self.delete)
        self.delete_button.grid(row=self.main_row_same, column=2, pady=5)

        # binding escape
        self.window.bind('<Escape>', self.back)

    def back(self, *args):
        return SearchWindow(self.window, MainWindow, self.query, self.search_phrase)

    def set_previous_button(self):
        if self.item_no == 0:
            previous_button = Button(self.window, text='<<', state=DISABLED)
            previous_button.grid(row=self.main_row, column=0, pady=5)
        else:
            previous_button = Button(
                self.window, text='<<', command=self.previous)
            previous_button.grid(row=self.main_row, column=0, pady=5)
            # binding left
            self.window.bind('<Left>', self.previous)

    def set_next_button(self):
        if self.item_no + 1 == len(self.query):
            next_button = Button(self.window, text='>>', state=DISABLED)
            next_button.grid(row=self.main_row_same, column=2, pady=5)
        else:
            next_button = Button(self.window, text='>>',
                                 command=self.next_meth)
            next_button.grid(row=self.main_row_same, column=2, pady=5)
            # binding right
            self.window.bind('<Right>', self.next_meth)

    def previous(self, *args):
        return DetailWindow(self.window, self.previous_window, self.item_no-1, self.query, self.search_phrase)

    def next_meth(self, *args):
        return DetailWindow(self.window, self.previous_window, self.item_no+1, self.query, self.search_phrase)

    def edit(self, *args):
        return UpdatePriceWindow(self.window, DetailWindow, self.item_no, self.query, self.search_phrase)

    def delete(self):
        response = messagebox.askyesno(
            'DELETE', 'Are you sure you want to delete entry?')
        if response == 1:
            delete_db(
                product_id=self.item[9],
                location_id=self.item[10]
            )
            query = search_db(self.search_phrase)
            return self.previous_window(self.window, MainWindow, query, self.search_phrase)

    def add_price(self):
        unit_number = float(self.item[2]) / float(self.item[12])
        product = (self.item[0], self.item[1],
                   self.item[3], unit_number, self.item[4])
        return CreateNewWindow(self.window, MainWindow, product=product)

# # # UPDATE PRICE # # #


class UpdatePriceWindow(Window):
    def __init__(self, window, previous_window, item_no, query, search_phrase):
        super().__init__(window, previous_window)
        self.item_no = item_no
        self.item = query[item_no]
        self.query = query
        self.search_phrase = search_phrase

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
        self.product_name_entry = Entry(self.product_name_frame, width=26)
        self.product_name_entry.grid(row=0, column=1)
        self.product_name_entry.insert(0, self.item[0])
        self.product_name_entry.configure(state=DISABLED)

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
        self.product_type_entry = Entry(self.product_type_frame, width=27)
        self.product_type_entry.grid(row=0, column=1)
        self.product_type_entry.insert(0, self.item[1])
        self.product_type_entry.configure(state=DISABLED)

        # PRICE
        # price frame
        self.price_frame = LabelFrame(window)
        self.price_frame.grid(row=self.main_row, column=0,
                              columnspan=2, pady=5)

        # price label
        self.price_label = Label(self.price_frame, text='Price:')
        self.price_label.grid(row=0, column=0)

        # price entry
        self.price_entry = Entry(self.price_frame, width=33)
        self.price_entry.grid(row=0, column=1)
        self.price_entry.insert(0, self.item[2])
        self.price_entry.focus_set()

        # CURRENCY AND UNIT
        # currency and unit frame
        self.currency_unit_frame = LabelFrame(window)
        self.currency_unit_frame.grid(
            row=self.main_row, column=0, columnspan=2, pady=5)

        # currency label
        self.currency_label = Label(self.currency_unit_frame, text='Currency:')
        self.currency_label.grid(row=0, column=0)

        # currency entry
        self.currency_entry = Entry(self.currency_unit_frame, width=6)
        self.currency_entry.grid(row=0, column=1)
        self.currency_entry.insert(0, self.item[3])

        # unit label
        self.unit_label = Label(self.currency_unit_frame, text='Unit:')
        self.unit_label.grid(row=0, column=2)

        # unit number
        self.unit_number = Entry(self.currency_unit_frame, width=6)
        self.unit_number.grid(row=0, column=3)
        self.get_unit_number = float(self.item[2]) / float(self.item[12])
        self.unit_number.insert(0, str(self.get_unit_number))

        # unit entry
        self.unit_entry = Entry(self.currency_unit_frame, width=12)
        self.unit_entry.grid(row=0, column=4)
        self.unit_entry.insert(0, self.item[4])

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
        self.location_name_entry = Entry(
            self.location_frame, width=25)
        self.location_name_entry.grid(row=0, column=1)
        self.location_name_entry.insert(0, self.item[5])
        self.location_name_entry.configure(state=DISABLED)

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
            self.general_location_frame, width=24)
        self.general_location_entry.grid(row=0, column=3)
        self.general_location_entry.insert(0, self.item[6])
        self.general_location_entry.configure(state=DISABLED)

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
        self.city_entry = Entry(self.city_frame, width=34)
        self.city_entry.grid(row=0, column=5)
        self.city_entry.insert(0, self.item[8])
        self.city_entry.configure(state=DISABLED)

        # CANCEL BUTTON
        self.cancel_button = Button(window, text='CANCEL', command=self.cancel)
        self.cancel_button.grid(row=self.main_row, column=0, pady=5)

        # UPDATE BUTTON
        self.update_execute_button = Button(
            window, text='UPDATE', command=self.update_execute)
        self.update_execute_button.grid(
            row=self.main_row_same, column=1, pady=5)

        # UPDATE PRODUCT BUTTON
        self.update_product_button = Button(
            self.window, text='EDIT PRODUCT', command=self.update_product)
        self.update_product_button.grid(row=self.main_row, column=0, pady=5)

        # UPDATE LOCATION BUTTON
        self.update_location_button = Button(
            self.window, text='EDIT LOCATION', command=self.update_location)
        self.update_location_button.grid(
            row=self.main_row_same, column=1, pady=5)

        # bind <Return> and <Escape>
        self.window.bind('<Return>', self.update_execute)
        self.window.bind('<Escape>', self.cancel)

    # update location
    def update_location(self):
        return UpdateLocationWindow(self.window, self.previous_window, self.item_no, self.query, self.search_phrase)

    # update product
    def update_product(self):
        return UpdateProductWindow(self.window, self.previous_window, self.item_no, self.query, self.search_phrase)

    def cancel(self, *args):
        return self.previous_window(self.window, SearchWindow, self.item_no, self.query, self.search_phrase)

    def update_execute(self, *args):
        # initiating validation
        if self.validate() is True:

            # creating full date
            submit_date = self.year_entry.get() + '-' + self.month_entry.get() + \
                '-' + self.day_entry.get()

            # creating price_per_unit
            price_per_unit = float(self.price_entry.get()) * \
                1 / float(self.unit_number.get())

            # submitting to database
            update_price_db(
                price=self.price_entry.get(),
                price_per_unit=str(price_per_unit),
                currency=self.currency_entry.get(),
                unit=self.unit_entry.get(),
                price_date=submit_date,
                product_id=self.item[9],
                location_id=self.item[10]
            )
            # getting new query and item number
            self.query = search_db(self.search_phrase)
            self.item_no = self.new_item_no

            return self.previous_window(self.window, SearchWindow, self.item_no, self.query, self.search_phrase)

    # getting new query
    @property
    def new_item_no(self):
        count = 0
        for item in self.query:
            if item[9] == self.item[9] and item[10] == self.item[10]:
                return count
            count += 1
        return MainWindow(self.window, MainWindow)

    def validate(self):
        # validating field length
        if len(self.price_entry.get()) == 0 or len(self.price_entry.get()) > 9:
            return self.warning()
        elif len(self.currency_entry.get()) == 0:
            return self.warning()
        elif len(self.unit_number.get()) == 0:
            return self.warning()
        elif len(self.unit_entry.get()) == 0:
            return self.warning()
        elif len(self.day_entry.get()) == 0 or len(self.day_entry.get()) > 2:
            return self.warning()
        elif len(self.month_entry.get()) == 0 or len(self.day_entry.get()) > 2:
            return self.warning()
        elif len(self.year_entry.get()) == 0 or len(self.day_entry.get()) > 4:
            return self.warning()

        # validating numbers
        try:
            float(self.price_entry.get())
            float(self.unit_number.get())
            if int(self.day_entry.get()) > 31 or int(self.day_entry.get()) < 1 or int(self.month_entry.get()) > 12 or int(self.month_entry.get()) < 1:
                return self.warning()
        except ValueError:
            return self.warning()
        return True

    # producing warning message
    @staticmethod
    def warning():
        return messagebox.showwarning('Warning', 'Entered fields are not valid')


# # # UPDATE PRODUCT # # #
class UpdateProductWindow(Window):
    def __init__(self, window, previous_window, item_no, query, search_phrase):
        super().__init__(window, previous_window)
        self.item_no = item_no
        self.item = query[item_no]
        self.query = query
        self.search_phrase = search_phrase
        self.picture = io.BytesIO()

        # PRODUCT NAME
        # product name frame
        self.product_name_frame = LabelFrame(window)
        self.product_name_frame.grid(
            row=self.main_row, column=0, columnspan=3, pady=5)

        # product name label
        self.product_name_label = Label(
            self.product_name_frame, text='Product name:')
        self.product_name_label.grid(row=0, column=0)

        # product name entry
        self.product_name_entry = Entry(self.product_name_frame, width=26)
        self.product_name_entry.grid(row=0, column=1)
        self.product_name_entry.insert(0, self.item[0])
        self.product_name_entry.focus_set()

        # PRODUCT TYPE
        # product type frame
        self.product_type_frame = LabelFrame(window)
        self.product_type_frame.grid(
            row=self.main_row, column=0, columnspan=3, pady=5)

        # product type label
        self.product_type_label = Label(
            self.product_type_frame, text='Product type:')
        self.product_type_label.grid(row=0, column=0)

        # product type entry
        self.product_type_entry = Entry(self.product_type_frame, width=27)
        self.product_type_entry.grid(row=0, column=1)
        self.product_type_entry.insert(0, self.item[1])

        # PRICE
        # price frame
        self.price_frame = LabelFrame(window)
        self.price_frame.grid(row=self.main_row, column=0,
                              columnspan=3, pady=5)

        # price label
        self.price_label = Label(self.price_frame, text='Price:')
        self.price_label.grid(row=0, column=0)

        # price entry
        self.price_entry = Entry(self.price_frame, width=33)
        self.price_entry.grid(row=0, column=1)
        self.price_entry.insert(0, self.item[2])
        self.price_entry.configure(state=DISABLED)

        # CURRENCY AND UNIT
        # currency and unit frame
        self.currency_unit_frame = LabelFrame(window)
        self.currency_unit_frame.grid(
            row=self.main_row, column=0, columnspan=3, pady=5)

        # currency label
        self.currency_label = Label(self.currency_unit_frame, text='Currency:')
        self.currency_label.grid(row=0, column=0)

        # currency entry
        self.currency_entry = Entry(self.currency_unit_frame, width=6)
        self.currency_entry.grid(row=0, column=1)
        self.currency_entry.insert(0, self.item[3])
        self.currency_entry.configure(state=DISABLED)

        # unit label
        self.unit_label = Label(self.currency_unit_frame, text='Unit:')
        self.unit_label.grid(row=0, column=2)

        # unit number
        self.unit_number = Entry(self.currency_unit_frame, width=6)
        self.unit_number.grid(row=0, column=3)
        self.get_unit_number = float(self.item[2]) / float(self.item[12])
        self.unit_number.insert(0, str(self.get_unit_number))
        self.unit_number.configure(state=DISABLED)

        # unit entry
        self.unit_entry = Entry(self.currency_unit_frame, width=12)
        self.unit_entry.grid(row=0, column=4)
        self.unit_entry.insert(0, self.item[4])
        self.unit_entry.configure(state=DISABLED)

        # LOCATION
        # location frame
        self.location_frame = LabelFrame(window)
        self.location_frame.grid(
            row=self.main_row, column=0, columnspan=3, pady=5)

        # location name label
        self.location_name_label = Label(
            self.location_frame, text='Location name:')
        self.location_name_label.grid(row=0, column=0)

        # location name entry
        self.location_name_entry = Entry(
            self.location_frame, width=25)
        self.location_name_entry.grid(row=0, column=1)
        self.location_name_entry.insert(0, self.item[5])
        self.location_name_entry.configure(state=DISABLED)

        # general location frame
        self.general_location_frame = LabelFrame(window)
        self.general_location_frame.grid(
            row=self.main_row, column=0, columnspan=3, pady=5)

        # general location label
        self.general_location_label = Label(
            self.general_location_frame, text='General location:')
        self.general_location_label.grid(row=0, column=2)

        # general location entry
        self.general_location_entry = Entry(
            self.general_location_frame, width=24)
        self.general_location_entry.grid(row=0, column=3)
        self.general_location_entry.insert(0, self.item[6])
        self.general_location_entry.configure(state=DISABLED)

        # DATE
        # date frame
        self.date_frame = LabelFrame(window)
        self.date_frame.grid(row=self.main_row, column=0, columnspan=3, pady=5)

        # date label
        self.location_name_label = Label(self.date_frame, text='Date:')
        self.location_name_label.grid(row=0, column=0)

        # date entry
        self.date_today = date.today()
        # day entry
        self.day_entry = Entry(self.date_frame, width=3)
        self.day_entry.grid(row=0, column=1)
        self.day_entry.insert(0, str(self.date_today)[8:])
        self.day_entry.configure(state=DISABLED)

        # month entry
        self.month_entry = Entry(self.date_frame, width=3)
        self.month_entry.grid(row=0, column=2)
        self.month_entry.insert(0, str(self.date_today)[5:7])
        self.month_entry.configure(state=DISABLED)

        # year entry
        self.year_entry = Entry(self.date_frame, width=5)
        self.year_entry.grid(row=0, column=3)
        self.year_entry.insert(0, str(self.date_today)[:4])
        self.year_entry.configure(state=DISABLED)

        # CITY
        # city frame
        self.city_frame = LabelFrame(window)
        self.city_frame.grid(row=self.main_row, column=0, columnspan=3, pady=5)
        # city label
        self.city_label = Label(self.city_frame, text='City:')
        self.city_label.grid(row=0, column=4)

        # city entry
        self.city_entry = Entry(self.city_frame, width=34)
        self.city_entry.grid(row=0, column=5)
        self.city_entry.insert(0, self.item[8])
        self.city_entry.configure(state=DISABLED)

        # ROTATE LEFT BUTTON
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.icon_directory = os.path.join(self.directory, 'icons')
        self.rotate_left_button = Button(self.window, command=self.rotate_left)
        self.rotate_left_button.img = ImageTk.PhotoImage(
            file=os.path.join(self.icon_directory, 'rotate-left.png'))
        self.rotate_left_button.configure(image=self.rotate_left_button.img)
        self.rotate_left_button.grid(row=self.main_row, column=0, pady=5)

        # UPLOAD BUTTON
        self.upload_button = Button(
            self.window, text='UPLOAD PICTURE', command=self.upload)
        self.upload_button.grid(row=self.main_row_same, column=1, pady=5)

        # ROTATE RIGHT BUTTON
        self.rotate_right_button = Button(
            self.window, command=self.rotate_right)
        self.rotate_right_button.img = ImageTk.PhotoImage(
            file=os.path.join(self.icon_directory, 'rotate-right.png'))
        self.rotate_right_button.configure(image=self.rotate_right_button.img)
        self.rotate_right_button.grid(row=self.main_row_same, column=2, pady=5)

        if self.item[11] is None:
            self.rotate_left_button.configure(state=DISABLED)
            self.rotate_right_button.configure(state=DISABLED)

        # CANCEL BUTTON
        self.cancel_button = Button(window, text='CANCEL', command=self.cancel)
        self.cancel_button.grid(row=self.main_row, column=0, pady=5)

        # UPDATE BUTTON
        self.update_execute_button = Button(
            window, text='UPDATE', command=self.update_execute)
        self.update_execute_button.grid(
            row=self.main_row_same, column=2, pady=5)

        # bind <Return> and <Escape>
        self.window.bind('<Return>', self.update_execute)
        self.window.bind('<Escape>', self.cancel)

    # ROTATE LEFT
    def rotate_left(self):
        img = ImagePIL.open(io.BytesIO(self.item[11]))
        rotated_img = img.rotate(90)
        rotated_img.save(self.picture, format='JPEG')

    # ROTATE RIGHT
    def rotate_right(self):
        img = ImagePIL.open(io.BytesIO(self.item[11]))
        rotated_img = img.rotate(270)
        rotated_img.save(self.picture, format='JPEG')

    # UPLOAD PICTURE

    def upload(self):
        # opening file browser
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title='Select picture',
            filetypes=(('all files', '*.*'),)
        )
        try:
            img = ImagePIL.open(filename)
        except UnidentifiedImageError:
            messagebox.showerror('Error', 'Unsupported image!')
        except AttributeError:
            pass
        else:
            # converting to RGB
            if img.mode != 'RGB':
                img.convert('RGB')

            # cropping image
            if img.size[0] > img.size[1]:
                x = (img.size[0] - img.size[1]) // 2
                cropped_img = img.crop((x, 0, img.size[0]-x, img.size[1]))
            elif img.size[0] < img.size[1]:
                x = (img.size[1] - img.size[0]) // 2
                cropped_img = img.crop((0, x, img.size[0], img.size[1]-x))
            else:
                cropped_img = img

            # resizing image
            cropped_img.thumbnail((1000, 1000))

            # converting to bytes
            self.picture = io.BytesIO()
            cropped_img.save(self.picture, format='JPEG', quality=30)

    # CANCEL

    def cancel(self, *args):
        return self.previous_window(self.window, SearchWindow, self.item_no, self.query, self.search_phrase)

    # UPDATE
    def update_execute(self, *args):
        # initiating validation
        if self.validate() is True:

            # submitting to database with no picture
            if len(self.picture.getvalue()) == 0:
                update_product_db(
                    product_name=self.product_name_entry.get(),
                    product_type=self.product_type_entry.get(),
                    product_id=self.item[9]
                )

            # submitting to database with picture
            else:
                update_product_db(
                    product_name=self.product_name_entry.get(),
                    product_type=self.product_type_entry.get(),
                    product_id=self.item[9],
                    picture=self.picture.getvalue()
                )

            # getting new query and item number
            self.query = search_db(self.search_phrase)
            self.item_no = self.new_item_no

            return self.previous_window(self.window, SearchWindow, self.item_no, self.query, self.search_phrase)

    # getting new query
    @property
    def new_item_no(self):
        count = 0
        for item in self.query:
            if item[9] == self.item[9] and item[10] == self.item[10]:
                return count
            count += 1
        return MainWindow(self.window, MainWindow)

    def validate(self):
        # validating field length
        if len(self.product_name_entry.get()) == 0:
            return self.warning()
        elif len(self.product_type_entry.get()) == 0:
            return self.warning()

        return True

    # producing warning message
    @staticmethod
    def warning():
        return messagebox.showwarning('Warning', 'Entered fields are not valid')


# # # -------------------- UPDATE LOCATION -------------------- # # #
class UpdateLocationWindow(Window):
    def __init__(self, window, previous_window, item_no, query, search_phrase):
        super().__init__(window, previous_window)
        self.item_no = item_no
        self.item = query[item_no]
        self.query = query
        self.search_phrase = search_phrase

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
        self.product_name_entry = Entry(self.product_name_frame, width=26)
        self.product_name_entry.grid(row=0, column=1)
        self.product_name_entry.insert(0, self.item[0])
        self.product_name_entry.configure(state=DISABLED)

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
        self.product_type_entry = Entry(self.product_type_frame, width=27)
        self.product_type_entry.grid(row=0, column=1)
        self.product_type_entry.insert(0, self.item[1])
        self.product_type_entry.configure(state=DISABLED)

        # PRICE
        # price frame
        self.price_frame = LabelFrame(window)
        self.price_frame.grid(row=self.main_row, column=0,
                              columnspan=2, pady=5)

        # price label
        self.price_label = Label(self.price_frame, text='Price:')
        self.price_label.grid(row=0, column=0)

        # price entry
        self.price_entry = Entry(self.price_frame, width=33)
        self.price_entry.grid(row=0, column=1)
        self.price_entry.insert(0, self.item[2])
        self.price_entry.configure(state=DISABLED)

        # CURRENCY AND UNIT
        # currency and unit frame
        self.currency_unit_frame = LabelFrame(window)
        self.currency_unit_frame.grid(
            row=self.main_row, column=0, columnspan=2, pady=5)

        # currency label
        self.currency_label = Label(self.currency_unit_frame, text='Currency:')
        self.currency_label.grid(row=0, column=0)

        # currency entry
        self.currency_entry = Entry(self.currency_unit_frame, width=6)
        self.currency_entry.grid(row=0, column=1)
        self.currency_entry.insert(0, self.item[3])
        self.currency_entry.configure(state=DISABLED)

        # unit label
        self.unit_label = Label(self.currency_unit_frame, text='Unit:')
        self.unit_label.grid(row=0, column=2)

        # unit number
        self.unit_number = Entry(self.currency_unit_frame, width=6)
        self.unit_number.grid(row=0, column=3)
        self.get_unit_number = float(self.item[2]) / float(self.item[12])
        self.unit_number.insert(0, str(self.get_unit_number))
        self.unit_number.configure(state=DISABLED)

        # unit entry
        self.unit_entry = Entry(self.currency_unit_frame, width=12)
        self.unit_entry.grid(row=0, column=4)
        self.unit_entry.insert(0, self.item[4])
        self.unit_entry.configure(state=DISABLED)

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
        self.location_name_entry = Entry(
            self.location_frame, width=25)
        self.location_name_entry.grid(row=0, column=1)
        self.location_name_entry.insert(0, self.item[5])
        self.location_name_entry.focus_set()

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
            self.general_location_frame, width=24)
        self.general_location_entry.grid(row=0, column=3)
        self.general_location_entry.insert(0, self.item[6])

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
        self.day_entry.configure(state=DISABLED)

        # month entry
        self.month_entry = Entry(self.date_frame, width=3)
        self.month_entry.grid(row=0, column=2)
        self.month_entry.insert(0, str(self.date_today)[5:7])
        self.month_entry.configure(state=DISABLED)

        # year entry
        self.year_entry = Entry(self.date_frame, width=5)
        self.year_entry.grid(row=0, column=3)
        self.year_entry.insert(0, str(self.date_today)[:4])
        self.year_entry.configure(state=DISABLED)

        # CITY
        # city frame
        self.city_frame = LabelFrame(window)
        self.city_frame.grid(row=self.main_row, column=0, columnspan=2, pady=5)
        # city label
        self.city_label = Label(self.city_frame, text='City:')
        self.city_label.grid(row=0, column=4)

        # city entry
        self.city_entry = Entry(self.city_frame, width=34)
        self.city_entry.grid(row=0, column=5)
        self.city_entry.insert(0, self.item[8])

        # CANCEL BUTTON
        self.cancel_button = Button(window, text='CANCEL', command=self.cancel)
        self.cancel_button.grid(row=self.main_row, column=0, pady=5)

        # UPDATE BUTTON
        self.update_execute_button = Button(
            window, text='UPDATE', command=self.update_execute)
        self.update_execute_button.grid(
            row=self.main_row_same, column=1, pady=5)

        # bind <Return> and <Escape>
        self.window.bind('<Return>', self.update_execute)
        self.window.bind('<Escape>', self.cancel)

    def cancel(self, *args):
        return self.previous_window(self.window, SearchWindow, self.item_no, self.query, self.search_phrase)

    def update_execute(self, *args):
        # initiating validation
        if self.validate() is True:

            # submitting to database
            update_location_db(
                location_name=self.location_name_entry.get(),
                city=self.city_entry.get(),
                general_location=self.general_location_entry.get(),
                location_id=self.item[10]
            )
            # getting new query and item number
            self.query = search_db(self.search_phrase)
            self.item_no = self.new_item_no

            return self.previous_window(self.window, SearchWindow, self.item_no, self.query, self.search_phrase)

    # getting new query
    @property
    def new_item_no(self):
        count = 0
        for item in self.query:
            if item[9] == self.item[9] and item[10] == self.item[10]:
                return count
            count += 1
        return MainWindow(self.window, MainWindow)

    def validate(self):
        # validating field length
        if len(self.location_name_entry.get()) == 0:
            return self.warning()
        elif len(self.general_location_entry.get()) == 0:
            return self.warning()
        elif len(self.city_entry.get()) == 0:
            return self.warning()

        return True

    # producing warning message
    @staticmethod
    def warning():
        return messagebox.showwarning('Warning', 'Entered fields are not valid')


# # # STARTING APP # # #
if __name__ == '__main__':
    root = Tk()
    MainWindow(root, MainWindow)
    root.mainloop()


# # # MOBILE REFERENCES # # #
# Canvas(width=1000, height=1800)
# separator: 70*'-'
# initialdir='/storage/emulated/0/DCIM/Camera'
# DetailWindow edit_button padx=86
# currency_entry width=7
# unit_number width=7
# unit_entry width=12
# SearchWindow wraplength=450
# DetailWindow wraplength=700
