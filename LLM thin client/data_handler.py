# data_handler.py
import threading

class DataHandler:
    def __init__(self):
        self.output_text_var = None
        self.text_font_family = "Times New Roman"
        self.font_size = 16
        self.wideFrame = 780
        self.narrowFrame = 210
        self.tallFrame = 455
        self.shortFrame = 195
        self.lock = threading.Lock()
        
        # Settings related variables
        self.selected_option = "OpenAI"
        self.endpoint = ""
        self.api_key = ""
        self.tokens_entry = "256"
        self.temperature = 1.0
        self.frequency_penalty = 1.0
        self.presence_penalty = 1.0
        self.top_p_sampling = 0.95
        self.user_name = ""

        # Variables for ButtonFrame interactions
        self.cached_context = ""
        self.old_context = ""
        self.new_message = ""
        self.assistant_focus = ""
        self.continue_generating = False
        self.play_hangman = False #this will be the variable that we'll be setting and getting as necessary
        self.mode_of_op = ""
        
    def set_output_text_var(self, output_text_var):
        self.output_text_var = output_text_var    

    def set_play_hangman(self, value):
        self.play_hangman = value

    def get_play_hangman(self):
        return self.play_hangman

    def set_RP(self, value):
        self.RP = value

    def get_RP(self):
        return self.RP
    
    @property
    def text_width(self):
        return self.wideFrame // self.font_size

    @property
    def text_font(self):
        return (self.text_font_family, self.font_size)
        
    # Getters and setters for settings variables
    def get_new_message(self):
        with self.lock:  # Acquire the lock before accessing/modifying the attribute
            return self.new_message
    
    def set_new_message(self, value):
        with self.lock:  # Acquire the lock before accessing/modifying the attribute
            self.new_message = value
    
    def get_assistant_focus(self):
        return self.assistant_focus
    
    def set_mode_of_op(self, value):
        with self.lock:  # Acquire the lock before accessing/modifying the attribute
            self.mode_of_op = value
    
    def get_mode_of_op(self):
        with self.lock:  # Acquire the lock before accessing/modifying the attribute
            return self.mode_of_op
    
    @property
    def set_assistant_focus(self, text_input):
        self.assistant_focus = text_input
    
    @property
    def get_selected_option(self):
        return self.selected_option

    @property
    def get_endpoint(self):
        return self.endpoint

    @property
    def get_api_key(self):
        return self.api_key

    @property
    def get_tokens_entry(self):
        return self.tokens_entry

    @property
    def get_temperature(self):
        return self.temperature

    @property
    def get_frequency_penalty(self):
        return self.frequency_penalty

    @property
    def get_presence_penalty(self):
        return self.presence_penalty

    @property
    def get_top_p_sampling(self):
        return self.top_p_sampling

    @property
    def get_user_name(self):
        return self.user_name

    def set_selected_option(self, value):
        self.selected_option = value

    def set_endpoint(self, value):
        self.endpoint = value

    def set_api_key(self, value):
        self.api_key = value

    def set_tokens_entry(self, value):
        self.tokens_entry = value

    def set_temperature(self, value):
        self.temperature = value

    def set_frequency_penalty(self, value):
        self.frequency_penalty = value

    def set_presence_penalty(self, value):
        self.presence_penalty = value

    def set_top_p_sampling(self, value):
        self.top_p_sampling = value

    def set_user_name(self, value):
        self.user_name = value

    # Getters and setters for ButtonFrame variables
    def get_cached_context(self):
        with self.lock:  # Acquire the lock before accessing/modifying the attribute
            return self.cached_context

    def set_cached_context(self, value):
        with self.lock:  # Acquire the lock before accessing/modifying the attribute
            self.cached_context = value

    def get_old_context(self):
        with self.lock:  # Acquire the lock before accessing/modifying the attribute
            return self.old_context

    def set_old_context(self, value):
        with self.lock:  # Acquire the lock before accessing/modifying the attribute
            self.old_context = value
        
    def set_continue_generating(self, value):
        with self.lock:  # Acquire the lock before accessing/modifying the attribute
            self.is_continue_generation = value
    
    def get_continue_generating(self):
        with self.lock:  # Acquire the lock before accessing/modifying the attribute
            return self.continue_generating


