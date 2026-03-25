import tkinter as tk
from tkinter import font
from context_menu import ContextMenu

class InputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.input_text_widget = None
        self.create_input_frame()

    def create_input_frame(self):
        input_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.shortFrame, bg='black')
        input_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        input_canvas.pack_propagate(False)

        text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)
        input_text = tk.Text(input_canvas, bg='#89BCEA', font=text_font, width=self.data_handler.text_width, wrap=tk.WORD)
        input_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.input_text_widget = input_text

        scrollbar = tk.Scrollbar(input_canvas, command=input_text.yview)
        scrollbar.pack(side='right', fill='y')
        input_text.config(yscrollcommand=scrollbar.set)

        context_menu = ContextMenu(input_text)
        input_text.bind("<Button-3>", context_menu.show_menu_input)
        input_text.insert(tk.END, "Please type here for automatic formatting")

    def clear_text_widget(self):
        self.input_text_widget.delete("1.0", tk.END)

    def return_text(self):
        return self.input_text_widget.get("1.0", tk.END).strip()