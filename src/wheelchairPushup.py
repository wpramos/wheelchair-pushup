# The application icon is downloaded from Freepik - Flaticon
# https://www.flaticon.com/free-icons/wheelchair

import tkinter as tk

root = tk.Tk()
root.title('Wheelchair Pushup')
root.geometry('300x150-0-100')
root.resizable(False, False)
root.attributes('-topmost', '1')
root.iconbitmap('img/wheelchairPushup.ico')

root.mainloop()
