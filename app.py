import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("My First App")
root.geometry("400x300")

# Add a label
label = ttk.Label(root, text="Hello, World!")
label.pack(pady=20)

# Add a button
def button_click():
    label.config(text="Button clicked!")

button = ttk.Button(root, text="Click Me!", command=button_click)
button.pack(pady=10)

# Start the app
root.mainloop()