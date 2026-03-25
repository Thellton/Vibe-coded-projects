import tkinter as tk
import context_menu

input_text_widget = None  # Global variable to hold the input text widget

def create_input_frame(window, widthIn, heightIn, text_font, text_width):
    global input_text_widget
    input_canvas = tk.Canvas(window, width=widthIn, height=heightIn, bg='black')
    input_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)
    input_canvas.pack_propagate(False)

    input_text = tk.Text(input_canvas, bg='#89BCEA', font=text_font, width=text_width, wrap=tk.WORD)
    input_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
    input_text_widget = input_text  # Assign the input text widget to the global variable

    scrollbar = tk.Scrollbar(input_canvas, command=input_text.yview)
    scrollbar.pack(side='right', fill='y')
    input_text.config(yscrollcommand=scrollbar.set)
    
    input_text.bind("<Button-3>", lambda event: context_menu.show_menu_input(input_text, event))
    input_text.insert(tk.END, "Please type here for automatic formatting")

def clear_text_widget():
    input_text_widget.delete("1.0", tk.END)

def return_text():
    return input_text_widget.get("1.0", tk.END).strip()

def main(window, widthIn, heightIn, text_font, text_width):
    create_input_frame(window, widthIn, heightIn, text_font, text_width)

if __name__ == "__main__":
    main()


'''
import tkinter as tk
import context_menu # assuming the context menu code is in a file named context_menu.py

def create_input_frame(window, widthIn, heightIn, text_font, text_width):
    # Create a Canvas widget for the output with the calculated size
    input_canvas = tk.Canvas(window, width=widthIn, height=heightIn, bg='black') #same as test
    input_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5) #same as test
    input_canvas.pack_propagate(False) #this prevents the canvas itself from resizing
    print(f"input_frame: step 1: element width: {widthIn}")
    print(f"step 1: element height: {heightIn}")

    # Create a Text widget and add it to the Canvas
    input_text = tk.Text(input_canvas, bg='#89BCEA', font=text_font, width=text_width) #same as test
    # Make the Text widget fill the Canvas
    input_text.pack(side='left', fill='both', expand=True, padx=5, pady=5) #same as test

    # Create and configure the Scrollbar
    scrollbar = tk.Scrollbar(input_canvas, command=input_text.yview) #same as test
    scrollbar.pack(side='right', fill='y') #same as test
    
    # Link the Scrollbar to the Text widget
    input_text.config(yscrollcommand=scrollbar.set) #same as test

    #output_canvas.create_window((0, 0), window=output_text, anchor='nw')
    
    #bind the button-3 event to the context menu
    input_text.bind("<Button-3>", lambda event: context_menu.show_menu_input(input_text, event))
   
    # Insert some initial text
    input_text.insert(tk.END, "Please type here for automatic formatting")

def main(window, widthIn, heightIn, text_font, text_width):
    # Create the output frame
    create_input_frame(window, widthIn, heightIn, text_font, text_width)

if __name__ == "__main__":
    main()

For the yellow square where the LLM’s output will be displayed, I would recommend using a Text widget in Tkinter. The Text widget is used for multi-line text fields where the user can enter text in more than one line. It can also be used to display text.

In this example, the create_output_frame function creates a Text widget with a yellow background (bg='yellow'). The width and height parameters determine the size of the text field. The padx and pady parameters to the pack method add some padding around the text field.

You can insert text into the Text widget using the insert method, and the END constant means that the text gets inserted at the end of the text field.

This is a basic example and you may need to adjust it to fit the needs of your application, such as adding scrollbars if the output is long. If you have any more questions or need further assistance, feel free to ask. 😊
'''
