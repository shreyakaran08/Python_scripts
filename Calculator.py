import tkinter as tk

# Creates a window
window = tk.Tk()
window.title("Calculator")

# Creates visual elements
label = tk.Label(window, text="Enter a number:")
entry = tk.Entry(window)  # Text input box
button = tk.Button(window, text="Double It!")
result_label = tk.Label(window, text="Result will appear here")


# Arranges elements on screen
label.pack()
entry.pack()
button.pack()
result_label.pack()

# Shows the window
window.mainloop()