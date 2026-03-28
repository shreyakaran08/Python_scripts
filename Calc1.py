import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.geometry("400x400")
        self.window.resizable(False, False)
        
        # Variables to store calculation data
        self.current = "0"
        self.previous = ""
        self.operation = ""
        self.should_reset = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Display frame
        display_frame = ttk.Frame(self.window, padding="10")
        display_frame.grid(row=0, column=0, sticky="ew")
        
        # Display entry
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.display = ttk.Entry(display_frame, textvariable=self.display_var, 
                                font=("Arial", 20), state="readonly", justify="right")
        self.display.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.window, padding="10")
        buttons_frame.grid(row=1, column=0)
        
        # Button layout
        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0), ('.', 4, 2), ('=', 4, 3)
        ]
        
        # Create buttons
        for (text, row, col) in buttons:
            if text == '0':
                # Make 0 button span 2 columns
                btn = ttk.Button(buttons_frame, text=text, width=5,
                               command=lambda t=text: self.on_button_click(t))
                btn.grid(row=row, column=col, columnspan=2, sticky="ew", padx=2, pady=2)
            else:
                btn = ttk.Button(buttons_frame, text=text, width=5,
                               command=lambda t=text: self.on_button_click(t))
                btn.grid(row=row, column=col, sticky="ew", padx=2, pady=2)
    
    def on_button_click(self, char):
        if char.isdigit():
            self.on_number(char)
        elif char == '.':
            self.on_decimal()
        elif char in '+-×÷':
            self.on_operation(char)
        elif char == '=':
            self.on_equals()
        elif char == 'C':
            self.on_clear()
        elif char == '±':
            self.on_sign_change()
        elif char == '%':
            self.on_percent()
    
    def on_number(self, num):
        if self.should_reset:
            self.current = "0"
            self.should_reset = False
        
        if self.current == "0":
            self.current = num
        else:
            self.current += num
        
        self.update_display()
    
    def on_decimal(self):
        if self.should_reset:
            self.current = "0"
            self.should_reset = False
        
        if '.' not in self.current:
            self.current += '.'
        
        self.update_display()
    
    def on_operation(self, op):
        if self.operation and not self.should_reset:
            self.on_equals()
        
        self.previous = self.current
        self.operation = op
        self.should_reset = True
    
    def on_equals(self):
        if self.operation and self.previous:
            try:
                # Convert operation symbols to Python operators
                op_map = {'+': '+', '-': '-', '×': '*', '÷': '/'}
                
                if self.operation == '÷' and float(self.current) == 0:
                    self.current = "Error"
                else:
                    result = eval(f"{self.previous} {op_map[self.operation]} {self.current}")
                    self.current = str(result)
                
                self.previous = ""
                self.operation = ""
                self.should_reset = True
                
            except:
                self.current = "Error"
                self.should_reset = True
        
        self.update_display()
    
    def on_clear(self):
        self.current = "0"
        self.previous = ""
        self.operation = ""
        self.should_reset = False
        self.update_display()
    
    def on_sign_change(self):
        if self.current != "0" and self.current != "Error":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
        
        self.update_display()
    
    def on_percent(self):
        try:
            result = float(self.current) / 100
            self.current = str(result)
            self.should_reset = True
            self.update_display()
        except:
            self.current = "Error"
            self.should_reset = True
            self.update_display()
    
    def update_display(self):
        # Format the display value
        if self.current == "Error":
            display_text = "Error"
        else:
            try:
                # Convert to float and back to remove unnecessary decimals
                num = float(self.current)
                if num == int(num):
                    display_text = str(int(num))
                else:
                    display_text = str(num)
            except:
                display_text = self.current
        
        self.display_var.set(display_text)
    
    def run(self):
        self.window.mainloop()

# Create and run the calculator
if __name__ == "__main__":
    calc = Calculator()
    calc.run()