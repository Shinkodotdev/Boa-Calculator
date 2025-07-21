import tkinter as tk
from tkinter import PhotoImage
from tkinter import scrolledtext  # Added for scrolled text


# Main Window
main_window = tk.Tk()
main_window.title("BOA")
main_window.config(bg="white")
main_window.geometry("215x500")
main_window.resizable(False, False)


# Adding light and dark mode images
light = PhotoImage(file="day-mode.png")
dark = PhotoImage(file="moon.png")
switch_value = True
history = []
# Circular buttons
buttons = [
    '%', 'CE', 'C', '←',
    '7', '8', '9', '*',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '.', '0', '/', '='
]
row_val = 2
col_val = 0
circular_buttons = []


def toggle():

    global switch_value

    if switch_value:
        input_entry.configure(bg="#26242f", fg="white", insertbackground="white")
        standard_label.configure(bg="#26242f", fg="white")
        switch_button.config(image=dark, bg="#26242f", activebackground="#26242f")
        main_window.config(bg="#26242f")
        history_button.config(bg="#26242f", fg="white")
        history_text.config(bg="#26242f", fg="white")

        switch_value = False

        for Button_to in circular_buttons:
            Button_to.configure(bg="#26242f", fg="white", highlightbackground="#26242f", activebackground="#26242f")
    else:
        input_entry.configure(bg="white", fg="black", insertbackground="black")
        standard_label.configure(bg="white", fg="black")
        switch_button.config(image=light, bg="white", activebackground="white")
        main_window.config(bg="white")
        history_button.config(bg="white", fg="black")
        history_text.config(bg="white", fg="black")

        switch_value = True

        # Change button colors to light mode
        for Button_to in circular_buttons:
            Button_to.configure(bg="white", fg="black", highlightbackground="white", activebackground="white")


def button_click(number):
    current = input_entry.get()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, current + str(number))


# clear field after enter
def clear():
    input_entry.delete(0, tk.END)


# calculate
def calculate():
    try:
        expression = input_entry.get()
        result = eval(expression)
        input_entry.delete(0, tk.END)
        input_entry.insert(0, str(result))

        # Append the calculation and result to the history
        history_item = f"{expression} = {result}"
        history.append(history_item)

        # Show the history after calculating
        show_history()

    except Exception:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, "Error")


# Show history
def show_history():
    history_text.config(state="normal")  # Enable the text widget for editing
    history_text.delete("1.0", tk.END)  # Clear the text widget

    for i, item in enumerate(history):
        history_text.insert(tk.END, f"{i + 1}. {item}\n")
    history_text.config(state="disabled")  # Disable the text widget after displaying


# Create a scrolled text widget for history
history_text = scrolledtext.ScrolledText(main_window, height=9, bg="white", fg="black", width=32, font=("Arial", 8))
history_text.grid(row=8, column=0, columnspan=5)


# Function to create circular buttons
def create_circle_button(text, row, col, command):

    circle_button = tk.Canvas(main_window, width=50, height=50, bg="#26242f", bd=0, highlightthickness=0)
    circle_button.grid(row=row, column=col, padx=1, pady=1)

    circle_button.create_oval(5, 5, 45, 45, fill="white", outline="#555")
    circle_button.create_text(25, 25, text=text, font=("Arial", 16), fill="black")

    circle_button.bind("<Button-1>", lambda event, cmd=command: cmd())

    return circle_button


# Function to add a decimal point ('.')
def add_decimal_point():

    current = input_entry.get()

    if '.' not in current:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, current + '.')


# Function to perform modulo operation ('%')
def calculate_modulo():

    expression = input_entry.get()

    if '%' in expression:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, "Invalid input")
    else:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, expression + '%')


# Function to handle backspace ('←')
def backspace():
    current = input_entry.get()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, current[:-1])


# Function to clear the history
def clear_history():
    global history
    history = []
    show_history()


# Clear History Button
history_button = tk.Button(main_window, bg="white", fg="black", text="Clear History", font=("Arial", 7), command=clear_history)
history_button.grid(row=10, column=2, columnspan=4)


# Welcome Label
standard_label = tk.Label(main_window, text="Shinko Calculator", font="Helvetica 10", bg="white", fg="black")
standard_label.grid(row=0, column=0, columnspan=4)


# Switch Toggle
switch_button = tk.Button(main_window, image=light, bd=0, bg="white", activebackground="white", command=toggle)
switch_button.grid(row=0, column=0)


# Input field calcu
input_entry = tk.Entry(main_window, font="Helvetica 20", insertwidth=10, width=14, justify="right", bg="white", fg="black")
input_entry.grid(row=1, column=0, columnspan=4)


button_actions = {
    "=": calculate,
    "CE": clear,
    "C": clear,
    ".": add_decimal_point,
    "%": calculate_modulo,
    "←": backspace
}

for button in buttons:
    if button in button_actions:
        action = button_actions[button]
    else:
        action = lambda num=button: button_click(num)

    create_circle_button(button, row_val, col_val, action)

    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Bind the "Enter" key to the calculate function
main_window.bind("<Return>", lambda event: calculate())

main_window.mainloop()