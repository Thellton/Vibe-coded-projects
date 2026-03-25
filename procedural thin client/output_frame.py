import tkinter as tk
from tkinter import font
import context_menu # assuming the context menu code is in a file named context_menu.py

def create_output_frame(window, widthIn, heightIn, output_text_var, text_font, text_width):
    print(f"{output_text_var.get()}:2")
    # Create a Canvas widget for the output with the calculated size
    output_canvas = tk.Canvas(window, width=widthIn, height=heightIn, bg='black')
    output_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5) 
    #output_canvas.pack_propagate(False) #this prevents the canvas itself from resizing
    print(f"output_frame: step 1: element width: {widthIn}")
    print(f"step 1: element height: {heightIn}")

    # Create a Text widget and add it to the Canvas
    print(f"output_frame: step 2: element width: {widthIn}")
    print(f"step 2: element height: {heightIn}")
    output_text = tk.Text(output_canvas, bg='#89BCEA', font=text_font, width=text_width, wrap=tk.WORD) 
    # Make the Text widget fill the Canvas
    output_text.pack(side='left', fill='both', expand=True, padx=5, pady=5) 

    # Create and configure the Scrollbar
    scrollbar = tk.Scrollbar(output_canvas, command=output_text.yview) 
    scrollbar.pack(side='right', fill='y') 
    
    # Link the Scrollbar to the Text widget
    output_text.config(yscrollcommand=scrollbar.set) 
    
    #bind the button-3 event to the context menu
    output_text.bind("<Button-3>", lambda event: context_menu.show_menu_output(output_text, event))
    
    # Insert some initial text
    output_text.insert(tk.END, "The current chat context will be displayed here in full, you can freely edit this if you prefer. use the continue button to tell the LLM to continue a sentence you or it wrote.", output_text_var.get())
    print(f"{output_text_var.get()}:3")

    def update_text(*args):
        #output_text.delete(1.0, tk.END) #this deletes the contents of the text widget
        #output_text.insert(tk.END, output_text_var.get()) #this inserts at the end of the text widget's text
        output_text.insert(tk.INSERT, output_text_var.get() + '\n') #this inserts at where the text cursor indicator/insertion cursor is
    
    output_text_var.trace("w", update_text)
    
    #returning output_text in the hopes that the utility_bar can get it
    return output_text
    
def main(window, widthIn, heightIn, output_text_var, text_font, text_width):
    # Create the output frame
    output_text = create_output_frame(window, widthIn, heightIn, output_text_var, text_font, text_width)
    return output_text

if __name__ == "__main__":
    root = tk.Tk()
    widthIn = 500
    heightIn = 500
    output_text_var = tk.StringVar()
    output_text_var.set("Initial text from utility_bar.py")
    text_font = ("Helvetica", 16)
    text_width = 50
    main(root, widthIn, heightIn, output_text_var, text_font, text_width)
    
    

'''
Hello! In tkinter, the width and height parameters for the tk.Text() widget are indeed in characters and lines respectively, not pixels. This is because tkinter was designed to be resolution independent and to work the same way on different display resolutions.

If you want to specify the size in pixels, you could use a tk.Canvas widget and add a tk.Text widget to it. The Canvas widget allows you to specify the size in pixels. 

In this code, the output_canvas is created with a size in pixels, and the output_text widget is added to the canvas. The text widget will fill the entire canvas, effectively giving you a text widget with a size specified in pixels. Please note that you might need to handle the scrollbars manually in this case. I hope this helps! Let me know if you have any other questions. 😊
'''

'''
Sure, you can enforce charWidth and charHeight to be integers by using the int() function in Python. This function will convert a float (or a valid string) into an integer. In this code, output_width / 4 and output_height / 4 are calculated as floats, and then int() is used to convert these values to integers. This ensures that charWidth and charHeight are integers, as expected by the tk.Text() function.

Please note that the int() function in Python performs floor division, which means it rounds down to the nearest whole number. If you want to round to the nearest whole number instead (either up or down), you can use the round() function:

To make the tk.Canvas widget stick to the left side of the window, you can use the pack() method with the anchor option set to 'w' (which stands for ‘west’). This will anchor the widget to the left side of its parent widget. However, if you want the Canvas widget to expand and shrink with the window, you might want to consider using the grid() geometry manager instead of pack(). The grid() method provides more control over how widgets are placed and resized. 

    # Create a Canvas widget for the output with the calculated size
    output_canvas = tk.Canvas(window, bg='yellow')
    output_canvas.grid(sticky='nsew')

    # Configure the grid to expand the Canvas widget when the window is resized
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)


In this code, the sticky='nsew' option makes the Canvas widget stick to all four sides of the window (north, south, east, and west), which means it will expand and shrink with the window. The grid_columnconfigure() and grid_rowconfigure() methods are used to tell tkinter that the Canvas widget should expand to take up any extra space when the window is resized.

I hope this helps! Let me know if you have any other questions. 😊
'''