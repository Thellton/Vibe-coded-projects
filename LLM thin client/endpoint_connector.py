import openai
import google.generativeai as genai
import os
import requests
import json
from data_handler import DataHandler

#https://github.com/BerriAI/litellm a universal caller for LLM API endpoints. could be described as being a phonebook...

class ResponseGenerator:
    def __init__(self, settings_frame, data_handler):
        self.settings_frame = settings_frame
        self.data_handler = data_handler
        self.parent = self
        self.gemini = EndpointConnectorGemini(settings_frame, data_handler)
        self.llamacpp = EndpointConnectorLLaMaCPP(settings_frame, data_handler)
    
    def categorise_response(self, prompt, completion_type):
        #this method categorises the particular response style between chat and text completion. this is also the best location in the program for determining whether to do complex agentic operations or not. it'd probably be a get call to a value held in data_handler that is set by the settings_frame.
        
        #I should put this in a loop with an escape condition agentic_operations being False, ie complete.
           
        if completion_type == "completion":
            print("getting text completion")
            return self.get_text_completion(prompt)
        elif completion_type == "chat":
            print("getting chat response")
            return self.get_chat_response(prompt)
        else: #retry
            print("getting a retry response")
            return self.get_chat_response(prompt)
        
            
    def get_text_completion(self, prompt):
        #need logic that will identify the relevant targeted EndpointConnector
        system_prompt = f"this is a text completion request, please complete it in keeping with the preceeding text that {self.settings_frame.return_username()} submits. endeavour to create text that smoothly integrates into the end of the text that {self.settings_frame.return_username()} provided. do not discuss this system prompt"
        
        if self.settings_frame.return_selected_option() == "Gemini":
            print("querying Gemini model") 
            return self.gemini.query_gemini_endpoint(prompt, system_prompt)
        else:
            print("querying LocalLLaMa model")
            Completion = True
            return self.llamacpp.query_llamacpp_endpoint_completion(prompt, system_prompt)
            
    def get_chat_response(self, prompt):
        #need logic that will identify the relevant targeted EndpointConnector
        system_prompt = f"this is a chat completion request, you are responding as {self.settings_frame.return_AI_name()} to {self.settings_frame.return_username()}'s question/interaction"
        
        if self.settings_frame.return_selected_option() == "Gemini":
            print("querying Gemini model")
            return self.gemini.query_gemini_endpoint(prompt,  system_prompt)
        else:
            print("querying LocalLLaMa model")
            return self.llamacpp.query_llamacpp_endpoint_chat(prompt, system_prompt)

    def get_first_character(self, text):
        return text[0] if text else ""
    
    
class EndpointConnectorLLaMaCPP:
    #https://github.com/ggerganov/llama.cpp/tree/master/examples/server
    def __init__(self, settings_frame, data_handler):
        self.settings_frame = settings_frame
        self.data_handler = data_handler

    def query_llamacpp_endpoint_chat(self, prompt, system_content, assistant_content=None, max_tokens=None):
        print("chat completion")
        #base_url = f"{self.settings_frame.return_endpoint()}v1/chat/completions"
        base_url = f"{self.settings_frame.return_endpoint()}v1"
        
        # Initialize the client with the determined base_url
        self.client = openai.OpenAI(
            api_key=self.settings_frame.return_api_key(),
            base_url=base_url,
        )

        # Prepare the messages payload
        input_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]

        if max_tokens is None:
            max_tokens = self.settings_frame.return_max_tokens()
            print(f"settings_frame.tokens_entry: {self.settings_frame.return_max_tokens()}")
            print(f"endpoint_connector.max_tokens: {max_tokens}")

        if assistant_content is not None:
            messages.insert(1, {"role": "assistant", "content": assistant_content})
        
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=input_messages,
                max_tokens=max_tokens,
                temperature=self.settings_frame.return_temp(),
                frequency_penalty=self.settings_frame.return_freq_pen(),
                presence_penalty=self.settings_frame.return_presence_pen(),
                top_p=self.settings_frame.return_top_P_sampling(),
                user=self.settings_frame.return_username()
            )
        except Exception as e:
            print(f"Error during API call: {e}")
            return None

          
        # Log the tokens generated and the response
        print(f"tokens generated: {completion.usage.completion_tokens}")
        print(f"response generated: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
       

class EndpointConnectorGemini:
    #https://ai.google.dev/gemini-api/docs/quickstart?lang=python
    def __init__(self, settings_frame, data_handler):
        self.settings_frame = settings_frame
        self.data_handler = data_handler
    
    def query_gemini_endpoint(self, prompt, system_content, assistant_content=None):
        genai.configure(api_key=self.settings_frame.return_api_key())
        
        input_prompt = f"system content contains general instructions for how to handle the response to the message history. message history contains all text that {self.settings_frame.return_username()} explicitly knows.  Latest message lists the most recent message from {self.settings_frame.return_username()}, so pay extra attention to it. " + f"n/n/system content: {system_content}" + f"n/n/assistant notes: {assistant_content}"+ f"n/n/message history: {prompt}" + f"n/n/latest message: {self.data_handler.get_new_message()}"
        
        if assistant_content != None:
            print("using assistant content")
            input_prompt = f"system content contains general instructions for how to handle the response to the message history. assistant notes contains information that you have be prompted to generate which is intended to augment your response to the message history. message history contains all text that {self.settings_frame.return_username()} explicitly knows. Latest message lists the most recent message from {self.settings_frame.return_username()}, so pay extra attention to it. " + f"n/n/system content: {system_content}" + f"n/n/assistant notes: {assistant_content}"+ f"n/n/message history: {prompt}" + f"n/n/latest message: {self.data_handler.get_new_message()}"
        
        print("trying to get a response")
        model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25') #gemini-1.5-flash
        response = model.generate_content(input_prompt)
        print("response generated")
                
        print(f"returning a response: {response.text}")
        return response.text #this is being returned to get_chat_response/get_text_completion

# Make the API call and handle exceptions
        '''
        if Comp_Chat == True:
            try:
                print(f"completions")
                completion = self.client.completions.create(
                    model="gpt-3.5-turbo",
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=self.settings_frame.return_temp(),
                    frequency_penalty=self.settings_frame.return_freq_pen(),
                    presence_penalty=self.settings_frame.return_presence_pen(),
                    top_p=self.settings_frame.return_top_P_sampling(),
                    user=self.settings_frame.return_username()
                )
            except Exception as e:
                print(f"Error during API call: {e}")
                return None
        else:
            try:
                print(f"chat")
                completion = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=prompt,
                    max_tokens=max_tokens,
                    temperature=self.settings_frame.return_temp(),
                    frequency_penalty=self.settings_frame.return_freq_pen(),
                    presence_penalty=self.settings_frame.return_presence_pen(),
                    top_p=self.settings_frame.return_top_P_sampling(),
                    user=self.settings_frame.return_username()
                )
            except Exception as e:
                print(f"Error during API call: {e}")
                return None
        '''     