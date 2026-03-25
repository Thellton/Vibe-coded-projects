import tkinter as tk

class SettingsFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.create_settings_frame()
        self.API_or_endpoint = "API"

    def create_settings_frame(self):
        self.settings_canvas = tk.Canvas(self.parent, width=self.data_handler.narrowFrame, height=self.data_handler.tallFrame, bg='#E7EAEA')
        self.settings_canvas.pack(side='left', fill='both', expand=True)

        settings_frame = tk.Frame(self.settings_canvas, bg='#E7EAEA')
        scrollbar = tk.Scrollbar(self.settings_canvas, command=self.settings_canvas.yview)
        scrollbar.pack(side='right', fill='y')

        self.settings_canvas.configure(yscrollcommand=scrollbar.set)
        self.settings_canvas.create_window((0, 0), window=settings_frame, anchor='nw')
        settings_frame.bind("<Configure>", lambda e: self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox("all")))

        tk.Label(settings_frame, text="API mode").pack()
        options = ["Gemini", "Local Endpoint"]
        self.selected_option = tk.StringVar(settings_frame)
        self.selected_option.set(options[0])
        option_menu = tk.OptionMenu(settings_frame, self.selected_option, *options)
        option_menu.pack()
        self.selected_option.trace("w", self.update_selected_option)

        self.endpoint_label = tk.Label(settings_frame, text="Endpoint to connect to")
        self.endpoint = tk.Entry(settings_frame, bg='#89BCEA')

        self.api_key_label = tk.Label(settings_frame, text="API key")
        self.api_key = tk.Entry(settings_frame, bg='#89BCEA')

        self.models_label = tk.Label(settings_frame, text="Select Model")
        self.models_option = tk.StringVar(settings_frame)
        self.models_menu = tk.OptionMenu(settings_frame, self.models_option, "")

        tk.Label(settings_frame, text="Tokens to Predict").pack()
        self.tokens_entry = tk.Entry(settings_frame, bg='#89BCEA')
        self.tokens_entry.insert(0, '256')
        self.tokens_entry.pack()

        tk.Label(settings_frame, text="Temperature").pack()
        self.temperature_scale = tk.Scale(settings_frame, from_=0, to=2, resolution=0.01, orient="horizontal")
        self.temperature_scale.set(1.0)
        self.temperature_scale.pack()

        tk.Label(settings_frame, text="Frequency Penalty").pack()
        self.frequency_penalty_scale = tk.Scale(settings_frame, from_=0, to=2, resolution=0.01, orient="horizontal")
        self.frequency_penalty_scale.set(1.0)
        self.frequency_penalty_scale.pack()

        tk.Label(settings_frame, text="Presence Penalty").pack()
        self.presence_penalty_scale = tk.Scale(settings_frame, from_=0, to=2, resolution=0.01, orient="horizontal")
        self.presence_penalty_scale.set(1.0)
        self.presence_penalty_scale.pack()

        tk.Label(settings_frame, text="Top-P Sampling").pack()
        self.top_p_sampling = tk.Scale(settings_frame, from_=0, to=1, resolution=0.01, orient="horizontal")
        self.top_p_sampling.set(0.95)
        self.top_p_sampling.pack()

        tk.Label(settings_frame, text="Username").pack()
        self.user_name = tk.Entry(settings_frame, bg='#89BCEA')
        self.user_name.insert(0, "Querant")
        self.user_name.pack()

        tk.Label(settings_frame, text="AI name").pack()
        self.AI_name = tk.Entry(settings_frame, bg='#89BCEA')
        self.AI_name.insert(0, "Respondent")
        self.AI_name.pack()

        self.settings_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.settings_canvas.bind_all("<Button-4>", self.on_mouse_wheel)
        self.settings_canvas.bind_all("<Button-5>", self.on_mouse_wheel)

        self.update_selected_option()

    def update_selected_option(self, *args):
        selected = self.selected_option.get()
        self.endpoint_label.pack_forget()
        self.endpoint.pack_forget()
        self.api_key_label.pack_forget()
        self.api_key.pack_forget()
        self.models_label.pack_forget()
        self.models_menu.pack_forget()

        if selected == "Local Endpoint":
            self.API_or_endpoint = "endpoint"
            self.endpoint_label.pack()
            self.endpoint.pack()
        else:
            self.API_or_endpoint = "API"
            self.api_key_label.pack()
            self.api_key.pack()
            self.models_label.pack()

        models = ["Gemini-1.0", "Gemini-1.5"]
        self.models_option.set(models[0])
        menu = self.models_menu["menu"]
        menu.delete(0, "end")
        for model in models:
            menu.add_command(label=model, command=lambda value=model: self.models_option.set(value))
        self.models_menu.pack()

    def on_mouse_wheel(self, event):
        if event.delta:
            self.settings_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            self.settings_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.settings_canvas.yview_scroll(1, "units")

    def return_API_or_endpoint(self):
        print(self.API_or_endpoint)
        return self.API_or_endpoint
    
    def return_model(self, value):
        #this might not work? I suspect there will be an issue with extracting the appropriate value from the array. arrays are pains in the ass...
        return self.models_option.get(models[value])
    
    def return_endpoint(self):
        print("entered return_endpoint code")
        #self.endpoint = tk.Entry(settings_frame, bg='#89BCEA') is this.
        endpoint = self.endpoint.get().strip()
        print(endpoint)
        return endpoint

    def return_max_tokens(self):
        try:
            return int(self.tokens_entry.get())
        except ValueError:
            return 256  # Default value

    def return_temp(self):
        return self.temperature_scale.get()

    def return_freq_pen(self):
        return self.frequency_penalty_scale.get()

    def return_presence_pen(self):
        return self.presence_penalty_scale.get()

    def return_top_P_sampling(self):
        return self.top_p_sampling.get()

    def return_username(self):
        return self.user_name.get()

    def return_selected_option(self):
        return self.selected_option.get()

    def return_api_key(self):
        api_key = self.api_key.get().strip()
        print(api_key)
        return api_key if api_key else "sk-no-key-required"

    def return_AI_name(self):
        #self.AI_name = tk.Entry(settings_frame, bg='#89BCEA') is this.
        return self.AI_name.get()