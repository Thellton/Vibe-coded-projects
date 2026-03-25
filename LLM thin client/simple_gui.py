import tkinter as tk
from tkinter import font
from data_handler import DataHandler
from context_menu import ContextMenu
import os
import json
from tkinter import messagebox
from endpoint_connector import ResponseGenerator
from input_frame import InputFrame
from output_frame import OutputFrame
from utility_bar import UtilityBar
from settings_frame import SettingsFrame
from button_frame import ButtonFrame


#I think I should break out these classes into their own modules.

class SimpleGUI:
    def __init__(self, root, data_handler):
        self.root = root
        self.data_handler = data_handler

        self.output_text_var = tk.StringVar()
        self.data_handler.set_output_text_var(self.output_text_var)

        self.text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)

        self.outputFrame = tk.Frame(self.root, bg="blue", width=self.data_handler.wideFrame, height=self.data_handler.tallFrame)
        self.inputFrame = tk.Frame(self.root, bg="red", width=self.data_handler.wideFrame, height=self.data_handler.shortFrame)
        self.settingsFrame = tk.Frame(self.root, bg="green", width=self.data_handler.narrowFrame, height=self.data_handler.tallFrame)
        self.buttonFrame = tk.Frame(self.root, bg="yellow", width=self.data_handler.narrowFrame, height=self.data_handler.shortFrame)
        
        self.setup_frames()
        self.input_frame = InputFrame(self.inputFrame, self.data_handler)
        self.output_frame = OutputFrame(self.outputFrame, self.data_handler)
        self.settings_frame = SettingsFrame(self.settingsFrame, self.data_handler)
        self.endpoint_connector = ResponseGenerator(self.settings_frame, self.data_handler)
        self.button_frame = ButtonFrame(self.buttonFrame, self.data_handler, self.input_frame, self.output_frame, self.settings_frame, self.endpoint_connector)
        self.utility_bar = UtilityBar(self.root, self.output_frame.output_text_widget, self.output_text_var, self.settings_frame, self.data_handler)

    def setup_frames(self):
        self.outputFrame.grid(row=0, column=0, sticky='nsew')
        self.inputFrame.grid(row=1, column=0, sticky='nsew')
        self.settingsFrame.grid(row=0, column=1, sticky='nsew')
        self.buttonFrame.grid(row=1, column=1, sticky='nsew')

    def run(self):
        self.root.mainloop()


    
if __name__ == "__main__":
    def main():
        root = tk.Tk()
        data_handler = DataHandler()
        gui = SimpleGUI(root, data_handler)
        gui.run()

    main()


