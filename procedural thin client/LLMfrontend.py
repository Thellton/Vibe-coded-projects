from tkinter import *
from tkinter import ttk, font
import tkinter as tk
import utility_bar 
import output_frame
import input_frame
import settings_frame
import button_frame

root = Tk()
root.title("LLM Thin Client")

output_text_var = tk.StringVar()

wideFrame = 780
narrowFrame = 210
tallFrame = 455
shortFrame = 195

font_size = 16
text_font = font.Font(family="Times New Roman", size=font_size)
text_width = wideFrame // font_size

outputFrame = Frame(root, bg="#E7EAEA", width=wideFrame, height=tallFrame)
inputFrame = Frame(root, bg="#E7EAEA", width=wideFrame, height=shortFrame)
settingsFrame = Frame(root, bg="#E7EAEA", width=narrowFrame, height=tallFrame)
buttonFrame = Frame(root, bg="#E7EAEA", width=narrowFrame, height=shortFrame)

outputFrame.grid(row=0, column=0, sticky='nsew')
inputFrame.grid(row=1, column=0, sticky='nsew')
settingsFrame.grid(row=0, column=1, sticky='nsew')
buttonFrame.grid(row=1, column=1, sticky='nsew')

output_text = output_frame.create_output_frame(outputFrame, wideFrame, tallFrame, output_text_var, text_font, text_width)
input_frame.create_input_frame(inputFrame, wideFrame, shortFrame, text_font, text_width)
settings_frame.create_settings_frame(settingsFrame, narrowFrame, tallFrame)
button_frame.create_button_frame(buttonFrame, narrowFrame, shortFrame, text_font)

button_frame.set_output_widget(output_text)  # Set the output text widget in button_frame

utility_bar.create_menu(root, output_text_var, output_text)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)

root.state('zoomed')
root.minsize(1020, 680)

root.mainloop()


'''
from tkinter import *
from tkinter import ttk, font 
import tkinter as tk
import utility_bar 
import output_frame
import input_frame
import settings_frame
import button_frame

# Create root window
root = Tk()
root.title("LLM Thin Client")

#getting the stringVar
output_text_var = tk.StringVar()

#frame variables
wideFrame = 780
narrowFrame = 210
tallFrame = 500
shortFrame = 150

#text variables
font_size = 16
text_font = font.Font(family="Times New Roman", size=font_size)
text_width = wideFrame//font_size

# Create the frames
outputFrame = Frame(root, bg="#E7EAEA", width=wideFrame, height=tallFrame)  # Specify width and height
inputFrame = Frame(root, bg="#E7EAEA", width=wideFrame, height=shortFrame)  # Specify width and height
settingsFrame = Frame(root, bg="#E7EAEA", width=narrowFrame, height=tallFrame)  # Specify width and height
buttonFrame = Frame(root, bg="#E7EAEA", width=narrowFrame, height=shortFrame)  # Specify width and height

# Establish the grid of frames using the grid() method
outputFrame.grid(row=0, column=0, sticky='nsew')
inputFrame.grid(row=1, column=0, sticky='nsew')
settingsFrame.grid(row=0, column=1, sticky='nsew')
buttonFrame.grid(row=1, column=1, sticky='nsew')

#stuffing stuff in the frames
output_text = output_frame.create_output_frame(outputFrame, wideFrame, tallFrame, output_text_var, text_font,text_width)
input_frame.create_input_frame(inputFrame, wideFrame, shortFrame, text_font,text_width)
settings_frame.create_settings_frame(settingsFrame, narrowFrame, tallFrame)
button_frame.create_button_frame(buttonFrame, narrowFrame, shortFrame, text_font)

# Create utility bar
utility_bar.create_menu(root, output_text_var, output_text)
print(f"{output_text_var.get()}:1")

#resizing
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)

# Launch in full screen (optional and system dependent)
root.state('zoomed')
root.minsize(1020, 680)

# Run the mainloop
root.mainloop()
'''


