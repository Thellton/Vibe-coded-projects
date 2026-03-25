import tkinter as tk
import threading

class ButtonFrame:
    def __init__(self, parent, DataHandler, InputFrame, OutputFrame, SettingsFrame, ResponseGenerator):
        self.parent = parent
        self.data_handler = DataHandler
        self.input_frame = InputFrame
        self.output_frame = OutputFrame
        self.settings_frame = SettingsFrame
        self.response_generator = ResponseGenerator
        self.create_button_frame()

    def create_button_frame(self):
        # This method creates the button frame for the application. It creates five buttons: "Submit prompt", "Continue generation", "Retry the generation", "Upload Image", and "Abort Generation". 
        button_frame = tk.Frame(self.parent, width=self.data_handler.narrowFrame, height=self.data_handler.shortFrame)
        button_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)

        button_width = 15
        button_height = 1
        text_font = self.data_handler.text_font

        tk.Button(button_frame, text="Submit prompt", width=button_width, height=button_height, font=text_font, command=self.submit_text).grid(column=1, row=0)
        tk.Button(button_frame, text="Continue generation", width=button_width, height=button_height, font=text_font, command=self.continue_generation).grid(column=1, row=1)
        tk.Button(button_frame, text="Retry the generation", width=button_width, height=button_height, font=text_font, command=self.retry_the_generation).grid(column=1, row=2)
        tk.Button(button_frame, text="Upload Image", width=button_width, height=button_height, font=text_font).grid(column=1, row=3)
        tk.Button(button_frame, text="Abort Generation", width=button_width, height=button_height, font=text_font).grid(column=1, row=4)

    def submit_text(self):
        # This method handles the "Submit prompt" button. It takes the text from the input field, formats it, adds it to the output display, and initiates a thread to fetch the response from the LLM. 
        if self.data_handler.output_text_var:
            user_text = self.input_frame.return_text() #obtaining the text from the input_text widget, ie the prompt
            user_name = self.settings_frame.return_username()
            AI_name = self.settings_frame.return_AI_name()
            user_text = f"\n\n{user_name}: {user_text} \n\n{AI_name}: " #formatting the text
            self.data_handler.set_new_message(user_text)
            self.input_frame.clear_text_widget() #clearing the input_text widget
            self.data_handler.set_cached_context(self.output_frame.output_text_widget.get("1.0", tk.END).strip()) #setting the current context, ie all prior prompts and responses
            LLM_input = self.data_handler.get_cached_context() + " " + user_text #concatenating the cached_context and the user_text variables to create the LLM_input
            self.output_frame.output_text_widget.insert(tk.END, user_text) #insert the user's text into the output_text widget
            self.data_handler.set_old_context(self.output_frame.output_text_widget.get("1.0", tk.END).strip()) 
            self.data_handler.set_continue_generating(False)
            self.data_handler.set_mode_of_op("chat")
            threading.Thread(target=self.fetch_response_completion, args=(LLM_input,)).start()


    def continue_generation(self):
        # This method handles the "Continue generation" button. It retrieves the current context from the output display and initiates a thread to fetch the continuation of the response from the LLM.
        if self.data_handler.output_text_var:
            self.data_handler.set_cached_context(self.output_frame.output_text_widget.get("1.0", tk.END).strip())
            self.data_handler.set_continue_generating(True)
            self.data_handler.set_mode_of_op("completion")
            threading.Thread(target=self.fetch_response_completion, args=(self.data_handler.get_cached_context(),)).start()

    def retry_the_generation(self):
        # This method handles the "Retry the generation" button. It retrieves the previous context from the output display and initiates a thread to fetch a new response from the LLM based on the previous prompt. 
        if self.data_handler.output_text_var:
            prompt_temperature = self.data_handler.get_temperature
            prompt_tokens = self.data_handler.get_tokens_entry
            self.data_handler.set_continue_generating(True)
            self.data_handler.set_mode_of_op("retry")
            threading.Thread(target=self.fetch_response_completion, args=(self.data_handler.get_old_context(),)).start()

    def fetch_response_completion(self, cached_context):
        # This method fetches the response from the LLM (using the ResponseGenerator object) and appends it to the output display.  It assumes a chat-based model. 
        #need a class/method that starts when this is called that starts a 'stopwatch' with a stop condition of a respsonse returning from query_openai_endpoint_text_completion_class_input. this will also require getting the endpoint to return a value for how many tokens were generated for the response, specifically 'completion_tokens'.
        print("beginning response completion process")
        mode_of_op = self.data_handler.get_mode_of_op()
        response = self.response_generator.categorise_response(cached_context, mode_of_op)
        self.output_frame.output_text_widget.insert(tk.END, f" {response}")
    
    #new method needed to save the state of the frontend that holds chat context and the settings used.