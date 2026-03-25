import tkinter as tk
import os
import json
from tkinter import messagebox, simpledialog, filedialog

class UtilityBar:        
    def __init__(self, window, output_frame, output_text_var, settings_frame, data_handler):
        self.window = window
        self.output_frame = output_frame
        self.output_text_var = output_text_var
        self.settings_frame = settings_frame
        self.create_menu()
        self.data_handler = data_handler


    def save(self):
        try:
            text = self.output_frame.get("1.0", "end-1c")
            file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt")
            if file_path:
                with open(file_path, "w", encoding ="utf-8") as file:
                    file.write(text)
                tk.messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while saving: {e}")

    def open_file(self):
        try:
            file_path = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "r", encoding ="utf-8") as file:
                    text = file.read()
                    self.output_frame.delete("1.0", tk.END)
                    self.output_frame.insert(tk.END, text)
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while opening the file: {e}")

    def load_text(self, file_path):
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while loading the file: {e}")
            return ""

    def create_menu(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        self.selected_mode = tk.StringVar()

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Save Settings", command=self.save_settings)
        file_menu.add_command(label="Load Settings", command=self.load_settings)
        file_menu.add_command(label="Restore Chat", command=self.open_file)
        file_menu.add_command(label="Save Chat", command=self.save)
        file_menu.add_command(label="Exit", command=self.window.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=lambda: self.output_frame.event_generate('<<Cut>>'))
        edit_menu.add_command(label="Copy", command=lambda: self.output_frame.event_generate('<<Copy>>'))
        edit_menu.add_command(label="Paste", command=lambda: self.output_frame.event_generate('<<Paste>>'))

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In")
        view_menu.add_command(label="Zoom Out")

        education_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Educational resources", menu=education_menu)
        education_menu.add_command(label="Chain of Thought", command=self.print_CoT)
        education_menu.add_command(label="Tree of Thought", command=self.print_ToT)

        mode_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Mode of Operation", menu=mode_menu)
        mode_menu.add_radiobutton(label="Chat mode", variable=self.selected_mode, value="chat")
        mode_menu.add_radiobutton(label="RP mode", variable=self.selected_mode, value="RP")
        mode_menu.add_radiobutton(label="Agent mode", variable=self.selected_mode, value="Agent")
        
        
    def print_CoT(self):
        text = self.load_text(os.path.join("education", "chain_of_thought.txt"))
        self.output_text_var.set(text)

    def print_ToT(self):
        text = self.load_text(os.path.join("education", "tree_of_thought.txt"))
        self.output_text_var.set(text)

    def get_mode_of_operation(self):
        return self.selected_mode
        
    def save_settings(self):
        endpoint_type = self.settings_frame.return_selected_option()
        
        print(self.settings_frame.return_selected_option())
        if endpoint_type == "OpenAI":
            settings = {
                "API_or_endpoint": "OpenAI",
                "api_key": self.settings_frame.return_api_key(),
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "user_name": self.settings_frame.return_username(),
                "AI_name": self.settings_frame.return_AI_name()
                #example of the resulting .json: {"API_or_endpoint": "OpenAI", "api_key": "example_APiKEY", "endpoint": "https://api.openai.com/v1/chat/completions", "user_name": "Querant", "AI_name": "Respondent"}
            }
        elif endpoint_type == "Gemini":
            settings = {
                "API_or_endpoint": "Gemini",
                "api_key": self.settings_frame.return_api_key(),
                "endpoint": None,
                "user_name": self.settings_frame.return_username(),
                "AI_name": self.settings_frame.return_AI_name()
                #example of the resulting .json: {"API_or_endpoint": "Gemini", "api_key": "example_APiKEY", "endpoint": null, "user_name": "Querant", "AI_name": "Respondent"}
                #Gemini endpoints are not supported as yet by endpoint_connector.py
            }
        else:
            settings = {
                "API_or_endpoint": "OpenAI compatible Endpoint",
                "api_key": None,
                "endpoint": self.settings_frame.return_endpoint(),
                "user_name": self.settings_frame.return_username(),
                "AI_name": self.settings_frame.return_AI_name()
                #example of the resulting .json:{"API_or_endpoint": "OpenAI compatible Endpoint", "api_key": null, "endpoint": "", "user_name": "Querant", "AI_name": "Respondent"}
            }
        
        # Prompt user for an optional filename
        filename = simpledialog.askstring("Save Settings", "Enter filename (leave blank for default):")
        if not filename:
            filename = "settings.json"
        else:
            filename += ".json"
        
        with open(filename, "w") as file:
            json.dump(settings, file)
        tk.messagebox.showinfo("Success", f"Settings saved successfully as {filename}!")
        
        #with open("settings.json", "w") as file:
        #    json.dump(settings, file)
        #tk.messagebox.showinfo("Success", "Settings saved successfully!")
        #I need to modify this so that the user can optionally set an alternative name for a settings file, rather  than the overwrite operation that we are presently using.

    def load_settings(self):
        def load_from_file(filename):
            with open(filename, "r") as file:
                settings = json.load(file)

                # Clear the widgets contents
                self.settings_frame.api_key.delete(0, tk.END)
                self.settings_frame.user_name.delete(0, tk.END)
                self.settings_frame.AI_name.delete(0, tk.END)
                self.settings_frame.endpoint.delete(0, tk.END)

                api_or_endpoint = settings.get("API_or_endpoint", "OpenAI")
                self.settings_frame.selected_option.set(api_or_endpoint)

                if api_or_endpoint == "OpenAI":
                    self.settings_frame.api_key.insert(0, settings.get("api_key", ""))
                    self.settings_frame.endpoint.insert(0, "https://api.openai.com/v1/chat/completions")
                elif api_or_endpoint == "Gemini":
                    self.settings_frame.api_key.insert(0, settings.get("api_key", "Gemini will need its own endpoint connector class damnit!"))
                    self.settings_frame.endpoint.insert(0, "")
                else:
                    self.settings_frame.endpoint.insert(0, settings.get("endpoint", ""))

                self.settings_frame.user_name.insert(0, settings.get("user_name", "Querant"))
                self.settings_frame.AI_name.insert(0, settings.get("AI_name", "Respondent"))
                self.settings_frame.update_selected_option()

                tk.messagebox.showinfo("Success", f"Settings loaded successfully from {filename}!")

        if os.path.exists("settings.json"):
            if tk.messagebox.askyesno("Load Settings", "Do you wish to load settings.json?"):
                load_from_file("settings.json")
            else:
                # Open a file dialog to select an alternative settings file
                filename = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
                if filename:
                    load_from_file(filename)
                else:
                    tk.messagebox.showinfo("Info", "No file selected, settings not loaded.")
        else:
            # If "settings.json" doesn't exist, directly open the file dialog
            tk.messagebox.showwarning("File Not Found", "settings.json not found. Please select an alternative settings file.")
            filename = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if filename:
                load_from_file(filename)
            else:
                tk.messagebox.showinfo("Info", "No file selected, settings not loaded.")


'''
    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                settings = json.load(file)

                #clear the widgets contents
                self.settings_frame.api_key.delete(0, tk.END)
                self.settings_frame.user_name.delete(0, tk.END)
                self.settings_frame.AI_name.delete(0, tk.END)
                self.settings_frame.endpoint.delete(0, tk.END)

                api_or_endpoint = settings.get("API_or_endpoint", "OpenAI")
                self.settings_frame.selected_option.set(api_or_endpoint)

                if api_or_endpoint == "OpenAI":
                    self.settings_frame.api_key.insert(0, settings.get("api_key", ""))
                    self.settings_frame.endpoint.insert(0, "https://api.openai.com/v1/chat/completions")
                elif api_or_endpoint == "Gemini":
                    self.settings_frame.api_key.insert(0, settings.get("api_key", "Gemini will need it's own endpoint connector class damnit!"))
                    self.settings_frame.endpoint.insert("")
                else:
                    self.settings_frame.endpoint.insert(0, settings.get("endpoint", ""))

                self.settings_frame.user_name.insert(0, settings.get("user_name", "Querant"))
                self.settings_frame.AI_name.insert(0, settings.get("AI_name", "Respondent"))
                self.settings_frame.update_selected_option()

                tk.messagebox.showinfo("Success", "Settings loaded successfully!")
        #I need to make it so that the program will first ask "do you wish to load settings.json" after having checked for a valid settings.json, if the user chooses no, the program will then open a file dialogue to allow loading an alternative valid .json file with user settings. this is to fascilitate switching between endpoint providers quickly with minimal disruption.
'''