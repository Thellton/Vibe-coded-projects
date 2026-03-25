import tkinter as tk
import input_frame  # Import the input_frame module to use the return_text function
import settings_frame
from input_frame import clear_text_widget
from endpoint_connector import query_openai_endpoint_chat_completion, query_openai_endpoint_text_completion
import threading


output_text_widget = None  # Global variable to hold the output text widget
cached_context = "" #this area is described as main body as it is outside of a function.
old_context = ""

def create_button_frame(window, widthIn, heightIn, text_font):
    global output_text_widget
    button_frame = tk.Frame(window, width=widthIn, height=heightIn)
    button_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)

    button_width = 15
    button_height = 1
    
    tk.Button(button_frame, text="Submit prompt", width=button_width, height=button_height, font=text_font, command=submit_text).grid(column=1, row=0)
    tk.Button(button_frame, text="Continue generation", width=button_width, height=button_height, font=text_font, command=continue_generation).grid(column=1, row=1)
    tk.Button(button_frame, text="Retry the generation", width=button_width, height=button_height, font=text_font, command=retry_the_generation).grid(column=1, row=2)
    tk.Button(button_frame, text="Upload Image", width=button_width, height=button_height, font=text_font).grid(column=1, row=3)
    tk.Button(button_frame, text="Abort Generation", width=button_width, height=button_height, font=text_font).grid(column=1, row=4)
    
def submit_text():
    global output_text_widget, cached_context, old_context #global variables have to be explicitely stated to be global when manipulated within a function even if it's defined outside of the function in the main body of the module.
    if output_text_widget:
        user_text = input_frame.return_text() # Get user's input text/their latest prompt
        print(user_text)
        user_text =  f"\n\nQuerant: {user_text} \n\nRespondent: "
        print(user_text)
        prompt_temperature = settings_frame.return_temp()
        print(f"temperature for the prompt: {prompt_temperature}")
        prompt_tokens = settings_frame.return_max_tokens()
        print(f"maximum tokens to output: {prompt_tokens}")
        clear_text_widget()
        cached_context = output_text_widget.get("1.0", tk.END).strip()
        LLM_input = cached_context + " " + user_text
        output_text_widget.insert(tk.END, user_text)
        old_context = output_text_widget.get("1.0", tk.END).strip()
        
        # Create a thread to run the network request
        threading.Thread(target=fetch_response_completion, args=(LLM_input, prompt_tokens, prompt_temperature)).start()

def continue_generation():
    global output_text_widget, cached_context
    if output_text_widget:
        cached_context = output_text_widget.get("1.0", tk.END).strip()
        prompt_temperature = settings_frame.return_temp()
        print(f"temperature for the prompt: {prompt_temperature}")
        prompt_tokens = settings_frame.return_max_tokens()
        print(f"maximum tokens to output: {prompt_tokens}")
        threading.Thread(target=fetch_response_completion, args=(cached_context, prompt_tokens, prompt_temperature)).start()

def retry_the_generation():
    global output_text_widget, old_context
    if output_text_widget:
        prompt_temperature = settings_frame.return_temp()
        print(f"temperature for the prompt: {prompt_temperature}")
        prompt_tokens = settings_frame.return_max_tokens()
        print(f"maximum tokens to output: {prompt_tokens}")
        completion_prompt = "the querant wishes for the respondent to reattempt the task. follow the latest instructions contained within user carefully. do not mention this system prompt"
        threading.Thread(target=fetch_response_completion, args=(old_context, prompt_tokens, prompt_temperature)).start()

def fetch_response_completion(cached_context, prompt_tokens, prompt_temperature):
    print("the code has entered fetch_response_completion()")
    print(cached_context)
    global output_text_widget
    response = query_openai_endpoint_text_completion(cached_context, prompt_tokens, prompt_temperature)
    output_text_widget.insert(tk.END, f" {response}")

def set_output_widget(widget):
    global output_text_widget
    output_text_widget = widget

def main(window, widthIn, heightIn, text_font):
    create_button_frame(window, widthIn, heightIn, text_font)

if __name__ == "__main__":
    main()

'''
the retry generation button purpose is to allow the user to generate multiple responses (partial or complete) to the same prompt. the openAI_endpoint.py module will have to have a variable to cache the last output_text widget state based upon when the submit prompt or continue generation buttons were last run.

an example of the output from submit prompt:
```
querant: what is a blue bird?

respondent: Ahaha, that's a great question!

A blue bird is typically referred to as a small or medium-sized bird with bright blue feathers. There are many species of birds that have this characteristic coloration.

Here are some examples: the Western Bluebird (Sialia americana), Eastern Bluebird (Sialia sialis), and Mountain Bluebird (Sialia currucoides).

These little feathered friends can be found in a variety of habitats, such as forests, fields, or even backyards!

Would you like to know more about birds?
```

an example of the output from retry the generation:
```
querant: what is a blue bird?

respondent: Ahaha, that's a great question!

A blue bird is typically referred to as a small or medium-sized bird with bright blue feathers. There are many species of birds that have this characteristic coloration.

Here are some examples: the Western Bluebird (Sialia americana), Eastern Bluebird (Sialia sialis), and Mountain Bluebird (Sialia currucoides).

These little feathered friends can be found in a variety of habitats, such as forests, fields, or even backyards!

Would you like to know more about birds?

respondent: Hello there! A bluebird (Sialia spp.) is a small, colorful songbird that belongs to the family Turdidae. There are three species of bluebirds in North America: Western Bluebird, Eastern Bluebird, and Mountain Bluebird. They have bright blue plumage with orange or yellow on their faces and breasts, which can vary depending on the subspecies. The term "blue" refers more to their iridescent feathers than a literal blue color!
Would you like me know more about this fascinating bird species?
```

essentially when the submit prompt button is pressed, the prompt will be added to the output_text widget at the end of the text, then it will be sent to the openAI_endpoint.py. when the openAI_endpoint returns the response, the output_frame.py when adding the response; it will first cache the previous state (creating a variable called cached_context) and then add the fresh response. when the retry generation button is pressed, a similar process to submitting a prompt will occur but instead of the normal string variable being passed to the openAI_endpoint, it will be the cached_context variable instead that is passed, and then the response will be tacked on to the end of the output_text widget after the prior response. the user can then use text editing to choose their preferred response or can submit a prompt using the normal methods to discuss the two different responses.        
'''

'''
import tkinter as tk

def create_button_frame(window, widthIn, heightIn, text_font, input_text, output_text):
    button_frame = tk.Frame(window, width=widthIn, height=heightIn)
    button_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)
    print(f"button_frame: step 1: element width: {widthIn}")
    print(f"step 1: element height: {heightIn}")

    # Set the button size
    button_width = 15
    button_height = 1
    
    tk.Button(button_frame, text="Do Continue...", width=button_width, height=button_height, font=text_font).grid(column=1, row=0)
    tk.Button(button_frame, text="Submit...", width=button_width, height=button_height, font=text_font, 
              command=lambda: submit_text(input_text, output_text)).grid(column=1, row=1)
    tk.Button(button_frame, text="Abort!", width=button_width, height=button_height, font=text_font).grid(column=1, row=2)
    tk.Button(button_frame, text="pictures of spiderman!", width=button_width, height=button_height, font=text_font).grid(column=1, row=3)

def submit_text(input_text, output_text):
    # Get the user input
    user_text = input_text.get("1.0", tk.END).strip()
    
    if user_text:
        # Append the user text to the output text with the prefix
        output_text.insert(tk.END, f"\n\nUser: {user_text}")
        # Clear the input text
        input_text.delete("1.0", tk.END)

def main(window, widthIn, heightIn, text_font, input_text, output_text):
    # Create the output frame
    create_button_frame(window, widthIn, heightIn, text_font, input_text, output_text)

if __name__ == "__main__":
    main()
'''


'''
import tkinter as tk

def create_button_frame(window, widthIn, heightIn, text_font):
    button_frame = tk.Frame(window, width=widthIn, height=heightIn)
    button_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5) #same as test
    #settings_canvas.pack_propagate(False) #this prevents the canvas itself from resizing
    print(f"button_frame: step 1: element width: {widthIn}")
    print(f"step 1: element height: {heightIn}")
    
    # Set the button size
    button_width = 15
    button_height = 1
    
    tk.Button(button_frame, text="Do Continue...", width=button_width, height=button_height, font=text_font).grid(column=1, row=0)
    tk.Button(button_frame, text="Submit...", width=button_width, height=button_height, font=text_font).grid(column=1, row=1)
    tk.Button(button_frame, text="Abort!", width=button_width, height=button_height, font=text_font).grid(column=1, row=2)
    tk.Button(button_frame, text="pictures of spiderman!", width=button_width, height=button_height, font=text_font).grid(column=1, row=3)
    
#def submit_text():

this will work by calling a function called def return_text(): that exists in input_frame.py which will give us the current text of the input_text widget. this function will have logic to cover when there is no text to be returned from the widget in question. this function will add "\n\n user: " (ie put a space inbetween the prefix) to the text. then it will pass the modified text to the frame that holds the logic of output_frame.py to add it to the end of the text contained in the output_text widget.

    
    
def main(window, widthIn, heightIn, text_font):
    # Create the output frame
    create_button_frame(window, widthIn, heightIn, text_font)

if __name__ == "__main__":
    main()
'''