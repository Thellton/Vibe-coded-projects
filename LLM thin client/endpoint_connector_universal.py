import openai
import google.generativeai as genai
import anthropic
import cohere
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
        self.openai = EndpointConnectorOpenAI(settings_frame, data_handler)
        self.gemini = EndpointConnectorGemini(settings_frame, data_handler)
        self.llamacpp = EndpointConnectorLLaMaCPP(settings_frame, data_handler)
        self.anthropic = EndpointConnectorAnthropic(settings_frame, data_handler)
        self.cohere = EndpointConnectorCohere(settings_frame, data_handler)
        self.llamacpp_agent = EndpointConnectorLLaMaCPPAgent(settings_frame, data_handler)
    
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
        
        if self.settings_frame.return_selected_option() == "OpenAI":  
            print("querying OpenAI model")
            return self.openai.query_openai_endpoint(prompt, system_prompt)
        elif self.settings_frame.return_selected_option() == "Gemini":
            print("querying Gemini model") 
            return self.gemini.query_gemini_endpoint(prompt, system_prompt)
        elif self.settings_frame.return_selected_option() == "LLaMa Agent":
            print("querying local llama agent")
            return self.llamacpp_agent.llama_agent(prompt, system_prompt)
        else:
            print("querying LocalLLaMa model")
            return self.llamacpp.query_llamacpp_endpoint(prompt, system_prompt)
            
    def get_chat_response(self, prompt):
        #need logic that will identify the relevant targeted EndpointConnector
        system_prompt = f"this is a chat completion request, you are responding as {self.settings_frame.return_AI_name()} to {self.settings_frame.return_username()}'s question/interaction"
        
        if self.settings_frame.return_selected_option() == "OpenAI": 
            print("querying OpenAI model")        
            return self.openai.query_openai_endpoint(prompt,  system_prompt)
        elif self.settings_frame.return_selected_option() == "Gemini":
            print("querying Gemini model")
            return self.gemini.query_gemini_endpoint(prompt,  system_prompt)
        elif self.settings_frame.return_selected_option() == "local llama agent":
            print("querying local llama agent")
            return self.llamacpp_agent.llama_agent(prompt, system_prompt)
        else:
            print("querying LocalLLaMa model")
            return self.llamacpp.query_llamacpp_endpoint(prompt,  system_prompt)

    def get_first_character(self, text):
        return text[0] if text else ""
        
class EndpointConnectorLLaMaCPPAgent:
    #the EndpointConnectorLLaMaCPPAgent class is intended for experimentation. the following are some concepts
    #1. a tree that asks the LLM questions about the intput/stimuli and helps shape how it wants to respond
    #2. a question that will ask the LLM how hard it thinks the creating an appropriate response to the input/stimuli will be; telling it to respond using a specific format to set a number of iterations (something textual, ie easy, medium, hard; corespond to 1, 3, and 5 iterations), whereupon it will loop creating a series of iterations to the input/stimuli, being asked at every iteration "is there anything you could do to improve on this?"
    def __init__(self, settings_frame, data_handler):
        self.settings_frame = settings_frame
        self.data_handler = data_handler
    
    def llama_agent(self, prompt, system_content):
        return self.iterative_agent(prompt, system_content)

    def iterative_agent(self, prompt, system_content):
        # First, ask the LLM to assess the difficulty of the task
        difficulty_prompt = f"Given the following task, assess its difficulty as 'easy', 'medium', or 'hard'. Respond with only one word. Task: {prompt}"
        difficulty = self.query_llamacpp_agent_endpoint(difficulty_prompt, system_content)
        print(f"LLaMa Agent rates the task difficulty as: {difficulty}")
        # Map difficulty to number of iterations
        iterations = {"easy": 3, "medium": 5, "hard": 7}.get(difficulty.lower().strip(), 3)
        
        # Generate initial response
        response = self.query_llamacpp_agent_endpoint(prompt, system_content)
        
        # Iterative improvement
        for _ in range(iterations - 1):  # -1 because we already have the initial response
            improve_prompt = f"Here's the current response to the task '{prompt}':\n\n{response}\n\nIs there anything you could do to improve on this? If yes, provide an improved version. If no, respond with 'No improvements needed.'"
            improvement = self.query_llamacpp_agent_endpoint(improve_prompt, system_content)
            
            if "No improvements needed" in improvement:
                break
            response = improvement
        
        return response

    def query_llamacpp_agent_endpoint(self, prompt, system_content, assistant_content=None, max_tokens=None):
        self.client = openai.OpenAI(
            api_key=self.settings_frame.return_api_key(),
            base_url=self.settings_frame.return_endpoint(),
        )
        
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]
        
        if max_tokens is None:
            max_tokens = self.settings_frame.return_max_tokens()
        
        if assistant_content is not None:
            messages.insert(1, {"role": "assistant", "content": assistant_content})
        
        print("presently inside query_llamacpp_agent_endpoint()")
        
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
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
        
        print(f"tokens generated: {completion.usage.completion_tokens}")
        print(f"response generated: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
    
    def load_questions(json_file):
        with open(json_file, 'r') as file:
            questions = json.load(file)
        return questions
        
    def get_first_character(self, text):
        return text[0] if text else ""

class EndpointConnectorOpenAI:
    #https://platform.openai.com/docs/api-reference/chat/create?lang=python
    #logit bias can be used ban certain tokens, or alternatively white list tokens so that a simple yes/no answer will be answered with yes/no and only "yes" or "no"
    def __init__(self, settings_frame, data_handler):
        self.settings_frame = settings_frame
        self.data_handler = data_handler
        #https://chatgpt.com/share/97513a88-8581-4879-82d0-b8fdaeac6590 - Lazy retrieval suggestions

    def query_openai_endpoint(self, prompt, system_content, assistant_content=None, max_tokens=None):
        
        self.client = openai.OpenAI(
            api_key=self.settings_frame.return_api_key(),
            base_url="https://api.openai.com/v1/chat/completions",
        )
        
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]
        
        if max_tokens == None:
            max_tokens = self.settings_frame.return_max_tokens()
            print(f"settings_frame.tokens_entry: {self.settings_frame.return_max_tokens()}")
            print(f"endpoint_connector.max_tokens: {max_tokens}")
            
        if assistant_content != None:
            messages.insert(1, {"role": "assistant", "content": assistant_content})
        
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
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

        print(f"tokens generated: {completion.usage.completion_tokens}")
        print(f"response generated: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
    
    
class EndpointConnectorLLaMaCPP:
    #https://github.com/ggerganov/llama.cpp/tree/master/examples/server
    def __init__(self, settings_frame, data_handler):
        self.settings_frame = settings_frame
        self.data_handler = data_handler
    
    def query_llamacpp_endpoint(self, prompt, system_content, assistant_content=None, max_tokens=None):
            
        self.client = openai.OpenAI(
            #base_url="http://192.168.68.111:6681/v1/",
            api_key=self.settings_frame.return_api_key(),
            base_url=self.settings_frame.return_endpoint(),
        )
        
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]
        
        if max_tokens == None:
            max_tokens = self.settings_frame.return_max_tokens()
            print(f"settings_frame.tokens_entry: {self.settings_frame.return_max_tokens()}")
            print(f"endpoint_connector.max_tokens: {max_tokens}")
            
        if assistant_content != None:
            messages.insert(1, {"role": "assistant", "content": assistant_content})
        
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
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

        print(f"tokens generated: {completion.usage.completion_tokens}")
        print(f"response generated: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
    
    def query_llamacpp_endpoint_streaming(self, prompt, system_content, assistant_content=None, max_tokens=None):
            
        self.client = openai.OpenAI(
            #base_url="http://192.168.68.111:6681/v1/",
            api_key=self.settings_frame.return_api_key(),
            base_url=self.settings_frame.return_endpoint(),
        )
        
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]
        
        if max_tokens == None:
            max_tokens = self.settings_frame.return_max_tokens()
            print(f"settings_frame.tokens_entry: {self.settings_frame.return_max_tokens()}")
            print(f"endpoint_connector.max_tokens: {max_tokens}")
            
        if assistant_content != None:
            messages.insert(1, {"role": "assistant", "content": assistant_content})
        
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
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

        for chunk in completion:
            return (chunk.choices[0].delta)
        
    def query_llamacpp_endpoint_completion(self, prompt, system_content, assistant_content=None, max_tokens=None):
            
        self.client = openai.OpenAI(
            #base_url="http://192.168.68.111:6681/v1/",
            api_key=self.settings_frame.return_api_key(),
            base_url= f"{self.settings_frame.return_endpoint()}v1,
        )
        
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]
        
        if max_tokens == None:
            max_tokens = self.settings_frame.return_max_tokens()
            print(f"settings_frame.tokens_entry: {self.settings_frame.return_max_tokens()}")
            print(f"endpoint_connector.max_tokens: {max_tokens}")
            
        if assistant_content != None:
            messages.insert(1, {"role": "assistant", "content": assistant_content})
        
        try:
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

        for chunk in completion:
            return (chunk.choices[0].delta)        
        
        #headers = {
        #'Content-Type': 'application/json',
        #}

        #json_data = {
        #'prompt': 'Building a website can be done in 10 simple steps:',
        #'n_predict': 128,
        #}

        #response = requests.post('http://localhost:8080/completion', headers=headers, json=json_data)

        # Note: json_data will not be serialized by requests
        # exactly as it was in the original request.
        #data = '{"prompt": "Building a website can be done in 10 simple steps:","n_predict": 128}'
        #response = requests.post('http://localhost:8080/completion', headers=headers, data=data)

class EndpointConnectorAnthropic:
    #https://docs.anthropic.com/en/docs/quickstart
    def __init__(self, settings_frame, data_handler):
        self.settings_frame = settings_frame
        self.data_handler = data_handler

    def query_anthropic_endpoint(self, prompt, system_content, assistant_content=None, max_tokens=None):
        self.client = anthropic.Anthropic(api_key=self.settings_frame.return_api_key())

        if max_tokens == None:
            max_tokens = self.settings_frame.return_max_tokens()
            print(f"settings_frame.tokens_entry: {self.settings_frame.return_max_tokens()}")
            print(f"endpoint_connector.max_tokens: {max_tokens}")

        #if assistant_content != None:
            #message.insert(1, {"role": "assistant", "content": [{"type": "text", "text": assistant_content]})
        #would it be possible to add api_key=self.settings_frame.return_api_key() to the self.client.messages.create()?
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=max_tokens,
                temperature=self.settings_frame.return_temp(),
                system=f"{system_content}",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
        except Exception as e:
            print(f"Error during API call: {e}")
            return None
        
        return (message.content)

class EndpointConnectorGemini:
    #https://ai.google.dev/gemini-api/docs/quickstart?lang=python
    def __init__(self, settings_frame, data_handler):
        self.settings_frame = settings_frame
        self.data_handler = data_handler
    
    def query_gemini_endpoint(self, prompt, system_content, assistant_content=None, max_tokens=None):
        #the issue doesn't originate from here...
        #chain of call query_gemini_endpoint > get_chat_response > categorise_response > button_frame > fetch_response_completion
        genai.configure(api_key=self.settings_frame.return_api_key())
        
        input_prompt = f"system content contains general instructions for how to handle the response to the message history. message history contains all text that {self.settings_frame.return_username()} explicitly knows.  Latest message lists the most recent message from {self.settings_frame.return_username()}, so pay extra attention to it. " + f"n/n/system content: {system_content}" + f"n/n/assistant notes: {assistant_content}"+ f"n/n/message history: {prompt}" + f"n/n/latest message: {self.data_handler.get_new_message()}"
        
        if assistant_content != None:
            print("using assistant content")
            input_prompt = f"system content contains general instructions for how to handle the response to the message history. assistant notes contains information that you have be prompted to generate which is intended to augment your response to the message history. message history contains all text that {self.settings_frame.return_username()} explicitly knows. Latest message lists the most recent message from {self.settings_frame.return_username()}, so pay extra attention to it. " + f"n/n/system content: {system_content}" + f"n/n/assistant notes: {assistant_content}"+ f"n/n/message history: {prompt}" + f"n/n/latest message: {self.data_handler.get_new_message()}"
        
        #try:
        print("trying to get a response")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(input_prompt)
        print("response generated")
        #except Exception as e:
        #    print(f"Error during API call: {e}")
        #    return None
        
        print(f"returning a response: {response.text}")
        return response.text #this is being returned to get_chat_response/get_text_completion
        
        
class EndpointConnectorCohere:
    #https://docs.cohere.com/docs/chat-api
    def __init__(self, settings_frame, data_handler):
        self.settings_frame = settings_frame
        self.data_handler = data_handler
    
    def query_cohere_endpoint(self, prompt, system_content, assistant_content=None, max_tokens=None):
        cohereAI = cohere.Client(api_key=self.settings_frame.return_api_key())
        input_prompt = f"system content contains general instructions for how to handle the response to the message history. message history contains all text that {self.settings_frame.return_username()} explicitly knows.  Latest message lists the most recent message from {self.settings_frame.return_username()}, so pay extra attention to it. " + f"n/n/system content: {system_content}" + f"n/n/assistant notes: {assistant_content}"+ f"n/n/message history: {prompt}" + f"n/n/latest message: {self.data_handler.get_new_message()}"
        
        if max_tokens == None:
            max_tokens = self.settings_frame.return_max_tokens()
            print(f"settings_frame.tokens_entry: {self.settings_frame.return_max_tokens()}")
            print(f"endpoint_connector.max_tokens: {max_tokens}")

        if assistant_content != None:
            input_prompt = f"system content contains general instructions for how to handle the response to the message history. assistant notes contains information that you have be prompted to generate which is intended to augment your response to the message history. message history contains all text that {self.settings_frame.return_username()} explicitly knows. Latest message lists the most recent message from {self.settings_frame.return_username()}, so pay extra attention to it. " + f"n/n/system content: {system_content}" + f"n/n/assistant notes: {assistant_content}"+ f"n/n/message history: {prompt}" + f"n/n/latest message: {self.data_handler.get_new_message()}"
        
        try:
            response = cohereAI.chat(
              model="command-r-plus",
              message=input_prompt 
            )
        except Exception as e:
            print(f"Error during API call: {e}")
            return None
            
        return(response.text) # "The Art of API Design: Crafting Elegant and Powerful Interfaces"


#"Step 2 of 6: before you write a response to the user's text, identify who you are roleplaying.", 
#"Step 3 of 6: before you write a response to the user's text, who are the other characters in the scene apart from the character you are roleplaying are. be suscinct in summarising.",
#"Step 4 of 6: before you write a response to the user's text, what are your character's observations of these characters? Which character is the most important for you to respond to? consider Theory of Mind when you write your character's observations.", 
#"Step 5 of 6: before you write a response to the user's text, how is your character inclined to act in this situation whilst considering these observations?",
#"Step 6 of 6: you may now write a draft response to the user's text making use of the conclusions you have drawn through steps 1 to 5."

#task 1: write a new endpoint connector that utilises llamacpp's native chat and text completion endpoints using cURL.
#task 2: alter the current endpoint connector so that it has a text completion option for chatGPT (compatibility subject to model...)
#task 3: write a new endpoint connector that is compatible with Google's Gemini (a free API is available) and Anthoropic's Claude API 

