import random
from tkinter import *
from playsound import playsound
import math
import json

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
reps = 0
timer = None
used_tips = []
cycles = 1


# Generate Tip
def generate_break_tip():
    with open("tips.json", "r") as file:
        data = json.load(file)
        new_tip = random.choice(data)
        if new_tip not in used_tips:
            tips_label.config(text=f"{new_tip['tip']}\n{new_tip['how']}")
            used_tips.append(new_tip)
        else:
            generate_break_tip()


# ------------------------ SOUNDS ----------------------#
def play_bell_1():
    playsound('bell_1.wav')


def play_bell_2():
    playsound('long_bell.wav')


# ---------------------------- TIMER RESET ------------------------------- #
def reset_button_clicked():
    global reps, used_tips
    reps = 0
    window.after_cancel(timer)
    timer_label.config(text="Timer", font=(FONT_NAME, 50, "normal"), bg=YELLOW, fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    check_marks.config(text="")
    tips_label.config(text="")
    used_tips = []


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_button_clicked():
    global reps, cycles
    reps += 1
    print(reps)

    if reps % 9 == 0:
        cycles += 1
        play_bell_2()
        reset_button_clicked()
        if cycles == 1:
            cycles_label.config(text=f"You have completed {cycles} cycle today.")
        else:
            cycles_label.config(text=f"You have completed {cycles} cycles today.")

    elif reps % 8 == 0:
        generate_break_tip()
        play_bell_1()
        count_down(LONG_BREAK_MIN * 60)
        timer_label.config(text="Long Break", fg=RED)

    elif reps % 2 == 0:
        play_bell_1()
        generate_break_tip()
        count_down(SHORT_BREAK_MIN * 60)
        timer_label.config(text="Break", fg=PINK)

    else:
        play_bell_1()
        count_down(WORK_MIN * 60)
        timer_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)

    else:
        raise_window(window)
        tips_label.config(text="")
        start_button_clicked()
        marks = ""
        work_sessions = math.floor(reps / 2)
        print(f"Work Sessions: {work_sessions}")
        for _ in range(work_sessions):
            marks += "🍅️"
        check_marks.config(text=marks, fg=GREEN, font=(FONT_NAME, 20, "normal"), bg=YELLOW, highlightbackground=YELLOW,
                           pady=10)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


# --------------------------- RAISE WINDOW ------------------------------ #
def raise_window(main_window):
    main_window.attributes('-topmost', 1)
    main_window.attributes('-topmost', 0)


# Timer Label
timer_label = Label(text="Timer", font=(FONT_NAME, 50, "normal"))
timer_label.config(bg=YELLOW, fg=GREEN)
timer_label.grid(column=1, row=0, pady=10)

tips_label = Label(text="", font=(FONT_NAME, 18, "bold"), anchor="w")
tips_label.config(bg=YELLOW, fg="black", pady=20, width=50)
tips_label.grid(columns=1, row=5, columnspan=3)

cycles_label = Label(text="", font=(FONT_NAME, 30, "normal"))
cycles_label.config(bg=YELLOW, fg="red")
cycles_label.grid(column=1, row=6)

# Image
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 135, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Buttons
start_button = Button(text="Start", font=(FONT_NAME, 10, "normal"), command=start_button_clicked)
start_button.config(bg=YELLOW, highlightbackground=YELLOW)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", font=(FONT_NAME, 10, "normal"), command=reset_button_clicked)
reset_button.config(bg=YELLOW, highlightbackground=YELLOW)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, font=(FONT_NAME, 10, "normal"), bg=YELLOW, highlightbackground=YELLOW, pady=10)
check_marks.grid(column=1, row=3)

window.mainloop()
