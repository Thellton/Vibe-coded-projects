import tkinter as tk
from tkinter import Menu, StringVar, filedialog, messagebox
import os

def save(frame):
    try:
        text = frame.get("1.0", "end-1c")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(text)
            messagebox.showinfo("Success", "File saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")

def open_file(frame):
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                text = file.read()
                frame.delete("1.0", tk.END)
                frame.insert(tk.END, text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening the file: {e}")

def load_text(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the file: {e}")
        return ""

def create_menu(window, output_text_var, frame):
    # Create a menu bar
    menubar = Menu(window)
    window.config(menu=menubar)

    # Create File menu
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New")
    file_menu.add_command(label="Open", command=lambda: open_file(frame))
    file_menu.add_command(label="Save", command=lambda: save(frame))
    file_menu.add_command(label="Exit", command=window.quit)

    # Create Edit menu
    edit_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Cut")
    edit_menu.add_command(label="Copy")
    edit_menu.add_command(label="Paste")

    # Create View menu
    view_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=view_menu)
    view_menu.add_command(label="Zoom In")
    view_menu.add_command(label="Zoom Out")
    
    # Create Instructions menu
    education_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Educational resources", menu=education_menu)
    
    def print_CoT():
        text = load_text(os.path.join("education", "chain_of_thought.txt"))
        output_text_var.set(text)
    
    def print_ToT():
        text = load_text(os.path.join("education", "tree_of_thought.txt"))
        output_text_var.set(text)
    
    education_menu.add_command(label="Chain of Thought", command=print_CoT)
    education_menu.add_command(label="Tree of Thought", command=print_ToT)
    
    
def main(window, output_text_var):
    frame = tk.Text(window, wrap="word")
    frame.pack(expand=True, fill="both")
    create_menu(window, output_text_var, frame)

if __name__ == "__main__":
    root = tk.Tk()
    output_text_var = StringVar()
    main(root, output_text_var)
    root.mainloop()


'''
import tkinter as tk
from tkinter import Menu, StringVar, filedialog, messagebox

def save(frame):
    try:
        text = frame.get("1.0", "end-1c")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(text)
            messagebox.showinfo("Success", "File saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")


def open_file(frame):
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                text = file.read()
                frame.delete("1.0", tk.END)
                frame.insert(tk.END, text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening the file: {e}")

def create_menu(window, output_text_var, frame):
    # Create a menu bar
    menubar = Menu(window)
    window.config(menu=menubar)

    # Create File menu
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New")
    file_menu.add_command(label="Open", command=lambda: open_file(frame))
    file_menu.add_command(label="Save", command=lambda: save(frame))
    file_menu.add_command(label="Exit", command=window.quit)

    # Create Edit menu
    edit_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Cut")
    edit_menu.add_command(label="Copy")
    edit_menu.add_command(label="Paste")

    # Create View menu
    view_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=view_menu)
    view_menu.add_command(label="Zoom In")
    view_menu.add_command(label="Zoom Out")
    
    # Create Instructions menu
    instructions_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Instructions", menu=instructions_menu)
    
    def print_CoT():
        output_text_var.set("chain of thought system prompt is an advanced prompting strategy to encourage reasoning in an LLM. broadly speaking, the model should respond to the phrase 'let's think step by step' by stating step by step it's observations about a task, in theory the model can then pause to and ask for the user's opinion, or proceed with writing a final response based upon it's observations of the task. the simplicity of the technique makes it very easy to use.")
    
    def print_ToT():
        output_text_var.set("A tree of thought prompt is an advanced prompting strategy to encourage reasoning in an LLM. \nThe following is an example of this: \n\n'Imagine three different experts are answering this question.All experts will write down 1 step of their thinking, then share it with the group. Then all experts will go on to the next step, etc. If any expert realises they're wrong at any point then they leave. The question is...' \n\nA variation of this prompt that I find produces interesting results is to name the experts, for this example we'll use authors. \n\n'Imagine three different experts in writing and story telling are working on writing their own continuation of the user's text. The experts are Ursula K. Le Guin, Stephen King, and Douglas Adams. All experts will write down 1 step of their thinking, then share it with the group. Then all experts will go on to the next step, etc. If any expert realises they're wrong at any point then they fall silent and instead contribute ideas to other experts. The text is...'\n\nI found the above to be quite powerful and in the case of Douglas Adams, funny. The above variation is rather specialised however, I feel it is demonstrative of another important consideration with LLMs, that being that a prompt that is specialised will draw more of the precise type of competence that the user needs out of the LLM in question.")
    
    instructions_menu.add_command(label="Chain of Thought", command=print_CoT)
    instructions_menu.add_command(label="Tree of Thought", command=print_ToT)
    
    
def main(window, output_text_var):
    frame = tk.Text(window, wrap="word")
    frame.pack(expand=True, fill="both")
    create_menu(window, output_text_var, frame)

if __name__ == "__main__":
    root = tk.Tk()
    output_text_var = StringVar()
    main(root, output_text_var)
    root.mainloop()
'''



'''
import tkinter as tk
from tkinter import Menu, StringVar, filedialog

def save(frame):
    try:
        text = frame.get("1.0", "end-1c")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")

def open_file(frame):
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                text = file.read()
                frame.delete("1.0", tk.END)
                frame.insert(tk.END, text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening the file: {e}")

    
def create_menu(window, output_text_var, frame):
    # Create a menu bar
    menubar = Menu(window)
    window.config(menu=menubar)

    # Create File menu
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New")
    file_menu.add_command(label="Open", menu=lambda:open_file(frame))
    file_menu.add_command(label="Save", command=lambda:save(frame))
    file_menu.add_command(label="Exit", command=window.quit)

    # Create Edit menu
    edit_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Cut")
    edit_menu.add_command(label="Copy")
    edit_menu.add_command(label="Paste")

    # Create View menu
    view_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=view_menu)
    view_menu.add_command(label="Zoom In")
    view_menu.add_command(label="Zoom Out")
    
    #create Instructions menu
    instructions_menu = Menu (menubar, tearoff=0)
    menubar.add_cascade(label="Instructions", menu=instructions_menu)
    
    # Define command functions to update the StringVar, the add_command widgets essentially allow the user to pull the lever that is these command functions.
    def print_CoT():
        output_text_var.set("chain of thought system prompt is an advanced prompting strategy to encourage reasoning in an LLM. broadly speaking, the model should respond to the phrase 'let's think step by step' by stating step by step it's observations about a task, in theory the model can then pause to and ask for the user's opinion, or proceed with writing a final response based upon it's observations of the task. the simplicity of the technique makes it very easy to use.")
    
    def print_ToT():
        output_text_var.set("A tree of thought prompt is an advanced prompting strategy to encourage reasoning in an LLM. \nThe following is an example of this: \n\n'Imagine three different experts are answering this question.All experts will write down 1 step of their thinking, then share it with the group. Then all experts will go on to the next step, etc. If any expert realises they're wrong at any point then they leave. The question is...' \n\nA variation of this prompt that I find produces interesting results is to name the experts, for this example we'll use authors. \n\n'Imagine three different experts in writing and story telling are working on writing their own continuation of the user's text. The experts are Ursula K. Le Guin, Stephen King, and Douglas Adams. All experts will write down 1 step of their thinking, then share it with the group. Then all experts will go on to the next step, etc. If any expert realises they're wrong at any point then they fall silent and instead contribute ideas to other experts. The text is...'\n\nI found the above to be quite powerful and in the case of Douglas Adams, funny. The above variation is rather specialised however, I feel it is demonstrative of another important consideration with LLMs, that being that a prompt that is specialised will draw more of the precise type of competence that the user needs out of the LLM in question.")
        print(f"{output_text_var.get()}:0")
    
    instructions_menu.add_command(label="Chain of Thought", command=print_CoT) #this provides the model with a means of concealing it's chain of thought by providing it an instruction and relevant tokens to work on concealling the model's working. in this mode of operation, the program will not stream the model's response until it recieves a closing tag.
    instructions_menu.add_command(label="Tree of Thought", command=print_ToT)  #this provides the model with a means of concealing it's Tree of thought py providing it an instruction and relevant tokens to work on concealling the model's workings. in this mode of operation, the program will not stream the model's response until it recieves a closing tag.
    
    
    
def main(window, output_text_var, frame):
    create_menu(window, output_text_var)

if __name__ == "__main__":
    root = tk.Tk()
    output_text_var = StringVar()
    main(root, output_text_var)
    root.mainloop()
'''


    #instructions_menu.add_command(label="Conceal Hangman") #essentially allows the model to conceal a single word for playing a game of hangman. simple.
    #instructions_menu.add_command(label="Emotion Engine") #tells the model to generate a concealled chain of thought that expresses their opinion of the the user/querant's interaction. the final step of the chain of thought is an emoticon from a curated list that will trigger the program to change a character image to reflect the mood.  
    #instructions_menu.add_command(label="A/B Preference Mode") #generate X number of responses from one endpoint, then create a match board and have the model judge which response was best of two responses. this will loop until all but one response has been eliminated.
    #instructions_menu.add_command(label="Ranked Choice Mode") #connect to multiple inference endpoints to generate a response, then have the models vote on the best response.
    #instructions_menu.add_command(label="Game Mode") #inputs a system prompt for playing a TTRPG/boardgame. this will require the frontend to be capable of uploading and submitting images to multimodal model.
    

