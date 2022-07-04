import math
import os
import pyautogui
import sys
from tkinter import *


# ---------------------------- CONSTANTS ------------------------------- #
GREEN = "#0085a1"
FONT_NAME = "Courier"


# ---------------------------- LOAD IMAGE ------------------------------- #
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    window.after_cancel(stop_count)
    mode_label.config(text="てるまーアプリ", fg=GREEN, font=(FONT_NAME, 35, "bold"))
    timer_canvas.itemconfig(timer_text, text="00:00")
    start_button.configure(text="START", command=lambda:[start_timer(), move_mouse_top(0, pyautogui.position())])
    canvas.itemconfig(canvas_image, image=top_image)


# ---------------------------- TIMER START ------------------------------- #
def start_timer():
    start_button.configure(text="STOP", command=reset_timer)
    mode_label.config(text="私はここにいるよ♪", font=(FONT_NAME, 30, "bold"))
    canvas.itemconfig(canvas_image, image=rest_image)
    count_up(0)


# ---------------------------- COUNT MECHANISM ------------------------------- #
def count_up(count):
    count_min = str(math.floor(count / 60))
    count_sec = str(count % 60)
    timer_canvas.itemconfig(timer_text, text=f"{count_min.zfill(2)}:{count_sec.zfill(2)}")
    global timer
    timer = window.after(1000, count_up, count + 1)


# ---------------------------- MOTION OF CURSOR ------------------------------- #
def move_mouse_gohey():
    r = 30
    (mx, my) = pyautogui.size()
    pyautogui.moveTo(round(mx/2), round(my/2 -r-r))
    move_num = 36
    for t in range(move_num):
        step = 1/move_num
        x = r*math.cos(step*t*2*math.pi)
        y = r*math.sin(step*t*2*math.pi)
        pyautogui.move(x,y)
    pyautogui.press('shift')


# ---------------------------- CURSOR MOVEMENT CHECK ------------------------------- #
def move_mouse_top(sleep_cnt, position):
    pos_current = pyautogui.position()
    dx = position.x - pos_current.x
    dy = position.y - pos_current.y
    dist = pow(dx * dx + dy * dy, 0.5)
    position = pos_current
    if dist < 20:
         sleep_cnt += 1
    else:
        sleep_cnt = 0
    if sleep_cnt > 180:  # <= How often do you move cursor?; sec
        move_mouse_gohey()
        sleep_cnt = 0
    global stop_count
    stop_count = window.after(1000, move_mouse_top, sleep_cnt, position)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Termar")
# window.iconbitmap("island.ico")
window.config(padx=100, pady=50, bg="white")


mode_label = Label(text="てるまーアプリ", font=(FONT_NAME, 35, "bold"), bg="white", foreground=GREEN)
mode_label.grid(column=1, row=0, pady=10)

canvas = Canvas(width=400, height=400, bg="white", highlightthickness=0)
top_image = PhotoImage(file=resource_path("nobi.png"))
top_image = top_image.zoom(40)
top_image = top_image.subsample(80)
rest_image = PhotoImage(file=resource_path("sabori.png"))
rest_image = rest_image.zoom(40)
rest_image = rest_image.subsample(80)
canvas_image = canvas.create_image(200, 200, image=top_image)
canvas.grid(column=1, row=1)

button_img = PhotoImage(file=resource_path("button.png"))
start_button = Button(text="START", font=("Arial", 14, "normal"), fg="white", image=button_img,  bg="white", activeforeground="white", activebackground="white", borderwidth=0, command=lambda:[start_timer(), move_mouse_top(0, pyautogui.position())], compound="center")
start_button.grid(column=0, row=2)

timer_canvas = Canvas(width=80, height=80, bg="white", highlightthickness=0)
timer_image = PhotoImage(file=resource_path("button.png"))
timer_canvas.create_image(40, 40, image=timer_image)
timer_text = timer_canvas.create_text(40, 40, text="00:00", fill="white", font=(FONT_NAME, 15, "bold"))
timer_canvas.grid(column=2, row=2)


# ---------------------------- MAIN ------------------------------- #
window.mainloop()