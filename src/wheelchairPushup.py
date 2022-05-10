# The application icon is downloaded from Freepik - Flaticon
# https://www.flaticon.com/free-icons/wheelchair

import logging

import math

import sys

import time

import tkinter as tk

import tkinter.ttk as ttk

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logging.disable()

sys_platform = sys.platform
logging.debug('sys_platform: {}'.format(sys_platform))

root = tk.Tk()
root.title('Wheelchair Pushup')
root.geometry('300x75-0-100')
root.resizable(False, False)
root.iconbitmap('img/wheelchairPushup.ico')


def resize_window_max():
    logging.debug('resize_window_max()')

    global is_window_maximized

    if not is_window_maximized:
        is_window_maximized = True

        # On Linux platforms, the state('zoomed') apparently returns an
        # exception when called, while on the Windows platform setting
        # the 'zoomed' attribute using the 'attribute' method raises an
        # exception. Mac too raises an exception similar to Windows.
        if sys_platform == 'linux':
            root.attributes('-zoomed', True)
        else:
            root.state('zoomed')


def resize_window_small():
    logging.debug('resize_window_small()')

    global is_window_maximized

    if is_window_maximized:
        is_window_maximized = False

        # On Linux platforms, the state() method apparently returns an
        # exception when called, while on the Windows platform setting
        # the 'zoomed' attribute using the 'attribute' method raises an
        # exception. Mac too raises an exception similar to Windows.
        if sys_platform == 'linux':
            root.attributes('-zoomed', False)
        else:
            root.state('normal')
        root.geometry('300x75-0-100')


pushup_timer = tk.StringVar()
label_pushup_timer = tk.Label(
    textvariable=pushup_timer,
    font=('TkDefaultFont', 144),
)

expected_pushup_time = 10
count = 0
is_pushup_timer_on = False


def run_pushup_timer(event=None):
    # This function serves both as an event handler, but is also called
    # independently. In the former case the event parameter is required.
    # However, if the function is called independently, the specified
    # parameter will be required. Hence, as a workaround the paremeter
    # 'event' is assigned a default value 'None'.
    logging.debug('run_pushup_timer()')

    global last_pushup_time, is_pushup_timer_on, count

    btn_start_pushup_timer.place_forget()
    label_pushup_timer.place(relx=0.5, rely=0.5, anchor='center')

    if not is_pushup_timer_on:
        count += 1
        is_pushup_timer_on = True
    else:
        pushup_timer.set(expected_pushup_time - count)

        if count > expected_pushup_time:
            is_pushup_timer_on = False
            count = 0
            last_pushup_time = time.time() - start_time
            deconstruct_pushup_window()
            return

        count += 1
    root.after(1000, run_pushup_timer)


btn_start_pushup_timer = ttk.Button(text='Start', command=run_pushup_timer)
btn_start_pushup_timer.bind('<Return>', run_pushup_timer)

start_time = time.time()

total_time = tk.StringVar()
label_total_time = tk.Label(textvariable=total_time)
label_total_time.place(relx=0.5, rely=0.5, anchor='center')


def to_hhmmss(seconds):
    hh = math.floor(seconds / 3600)
    seconds = seconds % 3600
    mm = math.floor(seconds / 60)
    ss = round(seconds % 60)

    if (ss < 10):
        ss = '0' + str(ss)
    elif (ss == 60):
        ss = '00'
        mm += 1

    if (hh == 0):
        return '{}:{}'.format(str(mm), ss)
    else:
        if (mm < 10):
            mm = '0' + str(mm)
        elif (mm == 60):
            mm = '00'
            hh += 1

        return '{}:{}:{}'.format(str(hh), mm, ss)


def update_total_time(seconds):
    logging.debug('update_total_time()')
    total_time.set(
        to_hhmmss(seconds)
    )


update_total_time(0)

last_pushup_time = 0
is_window_maximized = False


def construct_pushup_window():
    logging.debug('construct_pushup_window()')

    label_total_time.place_forget()

    resize_window_max()
    # deiconify() acts differrently based on the state of the window, at
    # least on my system. If the window is iconified, i.e. if the window
    # is minimized to to taskbar, deiconify() launches the window, with
    # focus. If the window is not iconified, but is simply hidden behind
    # other windows, deiconify() is restricted by Windows from launching
    # the window, but instead the method initiates a taskbar alert. As
    # the former action is desired, the root window is first iconified
    # before deiconification.
    root.iconify()
    root.deiconify()
    pushup_timer.set(expected_pushup_time)
    btn_start_pushup_timer.place(relx=0.5, rely=0.5, anchor='center')
    btn_start_pushup_timer.focus_set()


def deconstruct_pushup_window():
    logging.debug('deconstruct_pushup_window()')

    label_pushup_timer.place_forget()

    resize_window_small()
    label_total_time.place(relx=0.5, rely=0.5, anchor='center')


permissible_continuous_sitting_time = 150


def main_timed_function():
    logging.debug('main_timed_function()')

    total_time = time.time() - start_time
    update_total_time(total_time)

    continuous_sitting_time = total_time - last_pushup_time

    if (
        continuous_sitting_time >= permissible_continuous_sitting_time
        and not
        is_window_maximized
    ):
        construct_pushup_window()

    root.after(1000, main_timed_function)


main_timed_function()

root.mainloop()
