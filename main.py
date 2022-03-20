from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_face, image=front_card)
    flip_timer = window.after(3000, func=card_flip)


def card_flip():
    canvas.itemconfig(card_face, image=back_card)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=card_flip)

back_card = PhotoImage(file="./images/card_back.png")
correct = PhotoImage(file="./images/right.png")
correct_button = Button(image=correct, highlightbackground=BACKGROUND_COLOR, command=is_known)
correct_button.grid(column=1, row=2)

wrong = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong, highlightbackground=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=0, row=2)

canvas = Canvas(bg=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
front_card = PhotoImage(file="./images/card_front.png")
card_face = canvas.create_image(400, 263, image=front_card)
canvas.config(width=800, height=526)
card_title = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


next_card()

window.mainloop()
