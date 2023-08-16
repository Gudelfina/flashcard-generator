from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
card = {}
french_dict = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    french_dict = original_data.to_dict(orient="records")
else:
    french_dict = data.to_dict(orient="records")


def generate_word():
    global card, flip_timer

    window.after_cancel(flip_timer)

    card = random.choice(french_dict)

    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(french_word, text=card["French"])
    canvas.itemconfig(canvas_image, image=front_card_img)
    flip_timer = window.after(3000, func=english_card)


def english_card():
    canvas.itemconfig(canvas_image, image=back_card_img)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(french_word, text=card["English"])


def right_answer():
    global card
    french_dict.remove(card)
    data_to_learn = pandas.DataFrame(french_dict)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)

    generate_word()


window = Tk()
window.title("Learn French")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(4000, func=english_card)

canvas = Canvas(width=800, height=526)
front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_card_img)

# French/english words on flashcard canvas

card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill="black")
french_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=1, row=1, columnspan=2)

# Buttons

right_btn = PhotoImage(file="images/right.png")
right_button = Button(image=right_btn, highlightthickness=0, borderwidth=0, command=right_answer)
right_button.grid(column=2, row=2)

wrong_btn = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_btn, highlightthickness=0, borderwidth=0, command=generate_word)
wrong_button.grid(column=1, row=2)

generate_word()

window.mainloop()

