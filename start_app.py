from tkinter import *
import windows
from database import search_db

root = Tk()


# windows.MainWindow(root, windows.MainWindow)
query = search_db('mleko')
# print(query)
# windows.DetailWindow(root, windows.SearchWindow, query[0], 'mleko')
windows.SearchWindow(root, windows.MainWindow, 'mleko')
# Label(root, image=ImageTkPil.BitmapImage(ImagePil.open(io.BytesIO(query[0][1]))))

root.mainloop()
