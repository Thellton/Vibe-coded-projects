# context_menu.py

import tkinter as tk
from tkinter import filedialog
import os # Import the os module to work with file paths
import fitz # <-- Import PyMuPDF
import re   # <-- If using the cleaning example

# --- Keep or import your PDF extraction function ---
def extract_text_pymupdf_arxiv(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        print(f"Processing '{os.path.basename(pdf_path)}' with {doc.page_count} pages.")
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            page_text = page.get_text("text")
            # Optional basic cleaning (adjust as needed)
            # cleaned_page_text = "\n".join(line for line in page_text.split('\n') if len(line.strip()) > 20)
            # text += cleaned_page_text + "\n\n"
            text += page_text + "\n\n" # Simpler version without cleaning
        doc.close()
    except Exception as e:
        print(f"Error reading PDF with PyMuPDF: {e}")
        # Consider showing an error to the user via tk.messagebox
        # import tkinter.messagebox
        # tkinter.messagebox.showerror("PDF Error", f"Could not read PDF:\n{e}")
        return None # Return None on error
    return text.strip()
# --- End PDF extraction function ---

class ContextMenu:
    def __init__(self, frame):
        self.frame = frame
        # If you wanted an incrementing number instead of filename, you would initialize here:
        # self.resource_counter = 1

    def save_as_excerpt(self):
        # No changes needed here
        selected_text = ""
        try:
            # Get selected text only if there is a selection
            selected_text = self.frame.get("sel.first", "sel.last")
        except tk.TclError:
            # Handle cases where no text is selected gracefully (optional)
            print("No text selected to save.")
            return # Exit the function if no text is selected

        if selected_text: # Proceed only if text was selected
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(selected_text)
                except Exception as e:
                    print(f"Error saving file: {e}") # Basic error handling


    def load_excerpt(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    excerpt = file.read()

                # --- Modification Start ---
                # Get the filename without the extension
                filename = os.path.basename(file_path)
                resource_name = os.path.splitext(filename)[0]

                # Format the text with tags
                text_to_insert = f"<resource {resource_name}>\n{excerpt}\n</resource {resource_name}>\n"
                # --- Modification End ---

                # Insert the modified text at the current cursor position
                self.frame.insert(tk.INSERT, text_to_insert)

                # --- Alternative: Incrementing Number ---
                # If you wanted an incrementing number:
                # text_to_insert = f"<resource {self.resource_counter}>\n{excerpt}\n</resource {self.resource_counter}>\n"
                # self.frame.insert(tk.INSERT, text_to_insert)
                # self.resource_counter += 1
                # --- End Alternative ---
            except Exception as e:
                print(f"Error loading file: {e}") # Basic error handling


    def insert_excerpt(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
        if file_path:
            try:
                # Added encoding="utf-8" for consistency
                with open(file_path, "r", encoding="utf-8") as file:
                    excerpt = file.read()

                # --- Modification Start ---
                # Get the filename without the extension
                filename = os.path.basename(file_path)
                resource_name = os.path.splitext(filename)[0]

                # Format the text with tags
                text_to_insert = f"<resource {resource_name}>\n{excerpt}\n</resource {resource_name}>\n"
                # --- Modification End ---

                # Insert the modified text at the current cursor location
                self.frame.insert(tk.INSERT, text_to_insert)

                # --- Alternative: Incrementing Number ---
                # If you wanted an incrementing number:
                # text_to_insert = f"<resource {self.resource_counter}>\n{excerpt}\n</resource {self.resource_counter}>\n"
                # self.frame.insert(tk.INSERT, text_to_insert)
                # self.resource_counter += 1
                # --- End Alternative ---
            except Exception as e:
                print(f"Error inserting file: {e}") # Basic error handling
    
    # --- New Method for PDF Loading ---
    def load_pdf_content(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF File", # More specific title
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")] # Prioritize PDFs
        )
        if file_path:
            # Optional: Add user feedback like changing cursor while loading
            # self.frame.config(cursor="watch")
            # self.frame.update_idletasks()
            try:
                # Call the extraction function
                extracted_text = extract_text_pymupdf_arxiv(file_path)

                if extracted_text is not None: # Check if extraction was successful
                    filename = os.path.basename(file_path)
                    resource_name = os.path.splitext(filename)[0]

                    # Format the text with tags
                    text_to_insert = f"<resource {resource_name}>\n{extracted_text}\n</resource {resource_name}>\n"

                    # Insert the modified text at the current cursor position
                    self.frame.insert(tk.INSERT, text_to_insert)
                else:
                    # Error message already printed by the extraction function
                    # Optionally show a messagebox here too
                    pass

            except Exception as e:
                # Catch any unexpected errors during the process
                print(f"Error processing PDF file: {e}")
                # import tkinter.messagebox
                # tkinter.messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            # finally:
                # Restore cursor even if there was an error
                # self.frame.config(cursor="")

    def show_menu_output(self, event):
        # This menu seems intended for an output area, added Save/Insert
        context_menu = tk.Menu(self.frame, tearoff=0)
        context_menu.add_command(label="Cut", command=lambda: self.frame.focus_get().event_generate('<<Cut>>'))
        context_menu.add_command(label="Copy", command=lambda: self.frame.focus_get().event_generate('<<Copy>>'))
        context_menu.add_command(label="Paste", command=lambda: self.frame.focus_get().event_generate('<<Paste>>'))
        context_menu.add_separator() # Optional separator
        context_menu.add_command(label="Load Excerpt (.txt)", command=self.load_excerpt) # Clarify it's for .txt
        context_menu.add_command(label="Load PDF Content", command=self.load_pdf_content) # <-- Add the new command
        context_menu.add_separator() # Optional separator
        context_menu.add_command(label="Save as Excerpt", command=self.save_as_excerpt)
        context_menu.tk_popup(event.x_root, event.y_root)

    def show_menu_input(self, event):
        # This menu seems intended for an input area, added Load
        context_menu = tk.Menu(self.frame, tearoff=0)
        context_menu.add_command(label="Cut", command=lambda: self.frame.focus_get().event_generate('<<Cut>>'))
        context_menu.add_command(label="Copy", command=lambda: self.frame.focus_get().event_generate('<<Copy>>'))
        context_menu.add_command(label="Paste", command=lambda: self.frame.focus_get().event_generate('<<Paste>>'))
        context_menu.add_separator() # Optional separator
        context_menu.add_command(label="Load Excerpt", command=self.load_excerpt)
        # Save as Excerpt might also be useful here if the input area allows selection
        context_menu.add_command(label="Save as Excerpt", command=self.save_as_excerpt)
        context_menu.tk_popup(event.x_root, event.y_root)

# --- Main Function (for testing) ---
# Included basic error handling and slightly improved save function
# Also added filetypes to dialogs

def main():
    root = tk.Tk()
    root.title("Excerpt Test")

    # Example with two text widgets if you have separate input/output
    # Input Text
    input_frame = tk.Frame(root)
    input_frame.pack(pady=5, padx=5, fill="both", expand=True)
    input_label = tk.Label(input_frame, text="Input Area:")
    input_label.pack(anchor='w')
    input_text_widget = tk.Text(input_frame, height=10, width=60, undo=True)
    input_text_widget.pack(fill="both", expand=True)

    # Output Text (if applicable, otherwise just use one Text widget)
    output_frame = tk.Frame(root)
    output_frame.pack(pady=5, padx=5, fill="both", expand=True)
    output_label = tk.Label(output_frame, text="Output Area:")
    output_label.pack(anchor='w')
    output_text_widget = tk.Text(output_frame, height=10, width=60, state='disabled') # Example: Output might be read-only
    output_text_widget.pack(fill="both", expand=True)

    # Create separate context menu instances for each widget
    # If you only have one text widget in your actual GUI, just create one instance
    input_context_menu = ContextMenu(input_text_widget)
    input_text_widget.bind("<Button-3>", input_context_menu.show_menu_input)

    # If output area needs a menu (e.g., for copying or maybe inserting)
    output_context_menu = ContextMenu(output_text_widget)
    # Make output temporarily normal to allow binding, then disable again
    output_text_widget.config(state='normal')
    output_text_widget.bind("<Button-3>", output_context_menu.show_menu_output)
    output_text_widget.config(state='disabled')


    root.mainloop()

if __name__ == "__main__":
    main()