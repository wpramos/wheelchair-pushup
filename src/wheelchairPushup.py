# The application icon is downloaded from Freepik - Flaticon
# https://www.flaticon.com/free-icons/wheelchair

import logging

import math

import time

import tkinter as tk

import tkinter.ttk as ttk

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logging.disable()

root = tk.Tk()
root.title('Wheelchair Pushup')
root.geometry('300x150-0-100')
root.resizable(False, False)
root.iconbitmap('img/wheelchairPushup.ico')


def resize_fullscreen():
    logging.debug('resize_fullscreen()')

    global is_fullscreen

    if not is_fullscreen:
        is_fullscreen = True
        root.attributes('-topmost', True)
        root.attributes('-fullscreen', True)


def resize_small():
    logging.debug('resize_small()')

    global is_fullscreen

    if is_fullscreen:
        is_fullscreen = False
        root.attributes('-fullscreen', False)
        root.geometry('300x75-0-100')
        root.attributes('-topmost', False)


pushup_timer = tk.StringVar()
label_pushup_timer = tk.Label(textvariable=pushup_timer)

expected_pushup_time = 10
count = 0
is_pushup_timer_on = False


def run_pushup_timer():
    logging.debug('run_pushup_timer()')

    global last_pushup_time, is_pushup_timer_on, count

    btn_start_pushup_timer.pack_forget()

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

start_time = time.time()

total_time = tk.StringVar()
label_total_time = tk.Label(textvariable=total_time)
label_total_time.pack()


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
is_fullscreen = False


def construct_pushup_window():
    logging.debug('construct_pushup_window()')

    label_total_time.pack_forget()

    resize_fullscreen()
    pushup_timer.set(expected_pushup_time)
    label_pushup_timer.pack()
    btn_start_pushup_timer.pack()


def deconstruct_pushup_window():
    logging.debug('deconstruct_pushup_window()')

    label_pushup_timer.pack_forget()

    resize_small()
    label_total_time.pack()


permissible_continuous_sitting_time = 150


def main_timed_function():
    logging.debug('main_timed_function()')

    total_time = time.time() - start_time
    update_total_time(total_time)

    continuous_sitting_time = total_time - last_pushup_time

    if (
        continuous_sitting_time >= permissible_continuous_sitting_time
        and not
        is_fullscreen
    ):
        construct_pushup_window()

    root.after(1000, main_timed_function)


main_timed_function()

root.mainloop()
