import tkinter as tk
from tkinter import filedialog

def save_as_excerpt(frame):
    # Get the currently selected text
    selected_text = frame.get("sel.first", "sel.last")
    
    # Open a file dialog for the user to choose where to save the excerpt
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    
    # Write the selected text to the file
    with open(file_path, "w") as file:
        file.write(selected_text)

def load_excerpt(frame):
    # Open a file dialog for the user to choose a file
    file_path = filedialog.askopenfilename(defaultextension=".txt")
    
    # Read the contents of the file
    with open(file_path, "r") as file:
        excerpt = file.read()
    
    # Insert the contents into the Text widget
    frame.insert(tk.END, excerpt)

def insert_excerpt(frame):
    # Open a file dialog for the user to choose a file
    file_path = filedialog.askopenfilename(defaultextension=".txt")
    
    # Read the contents of the file
    with open(file_path, "r") as file:
        excerpt = file.read()
        
    # Insert the contents into the Text widget
    frame.insert(tk.END, excerpt) #need to change this to the cursor location

def show_menu_output(frame, event):
    context_menu = tk.Menu(frame, tearoff=0)
    context_menu.add_command(label="Cut", command=lambda: frame.focus_get().event_generate('<<Cut>>'))
    context_menu.add_command(label="Copy", command=lambda: frame.focus_get().event_generate('<<Copy>>'))
    context_menu.add_command(label="Paste", command=lambda: frame.focus_get().event_generate('<<Paste>>'))
    context_menu.add_command(label="Save as Excerpt", command=lambda: save_as_excerpt(frame))
    context_menu.add_command(label="Insert Except", command=lambda: insert_excerpt(frame))

    context_menu.tk_popup(event.x_root, event.y_root)

def show_menu_input(frame, event):
    context_menu = tk.Menu(frame, tearoff=0)
    context_menu.add_command(label="Cut", command=lambda: frame.focus_get().event_generate('<<Cut>>'))
    context_menu.add_command(label="Copy", command=lambda: frame.focus_get().event_generate('<<Copy>>'))
    context_menu.add_command(label="Paste", command=lambda: frame.focus_get().event_generate('<<Paste>>'))
    context_menu.add_command(label="Load Excerpt", command=lambda: load_excerpt(frame))

    context_menu.tk_popup(event.x_root, event.y_root)

def main():
    root = tk.Tk()
    text_widget = tk.Text(root)
    text_widget.pack()

    text_widget.bind("<Button-3>", lambda event: show_menu(text_widget, event))

    root.mainloop()

if __name__ == "__main__":
    main()
