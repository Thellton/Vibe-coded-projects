import tkinter as tk
from tkinter import font
from context_menu import ContextMenu

class OutputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.output_text_widget = None
        self.create_output_frame()

    def create_output_frame(self):
        output_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.tallFrame, bg='black')
        output_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)

        text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)
        output_text = tk.Text(output_canvas, bg='#89BCEA', font=text_font, width=self.data_handler.text_width, wrap=tk.WORD)
        output_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.output_text_widget = output_text

        scrollbar = tk.Scrollbar(output_canvas, command=output_text.yview)
        scrollbar.pack(side='right', fill='y')
        output_text.config(yscrollcommand=scrollbar.set)

        context_menu = ContextMenu(output_text)
        output_text.bind("<Button-3>", context_menu.show_menu_output)
        output_text.insert(tk.END, "The current chat context will be displayed here in full, you can freely edit this if you prefer. use the continue button to tell the LLM to continue a sentence you or it wrote.", self.data_handler.output_text_var.get())

        self.data_handler.output_text_var.trace("w", self.update_text)

    def update_text(self, *args):
        self.output_text_widget.insert(tk.INSERT, self.data_handler.output_text_var.get() + '\n')