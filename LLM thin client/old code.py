'''
import openai
from data_handler import DataHandler 

def query_openai_endpoint_text_completion_class_input(prompt, settings_frame):
    client = openai.OpenAI(
        base_url="http://192.168.68.111:6681/v1/", # this will require a variable that takes data from settings_frame.py
        api_key = settings_frame.return_api_key()
    )

    completion = client.chat.completions.create( 
        model="gpt-3.5-turbo", # this will need a variable passed when this function is called
        messages=[
            {"role": "system", "content": "this is a text completion request, please complete it in keeping with the text that the user submits."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=settings_frame.return_max_tokens(), 
        temperature=settings_frame.return_temp(), 
        frequency_penalty=settings_frame.return_freq_pen(),
        presence_penalty=settings_frame.return_presence_pen(),
        top_p=settings_frame.return_top_P_sampling(),
        user=settings_frame.return_username()
    )
    
    print(f"Diagnostics: response: {completion.choices[0].message.content}")
    return completion.choices[0].message.content
    
    def roleplay_step(self, prompt, step_description, assistant_content=None):
        system_content = f"Summarise {step_description}"
        return self.query_openai_endpoint(prompt, system_content, assistant_content)

    def get_first_character(self, text):
        return text[0] if text else ""

    def get_chat_response(self, prompt):
        RP = False
        continue_generating = self.data_handler.get_continue_generating()
        print(f"continue_generating: {continue_generating}")
        
        if RP == True:
            print("entering RP classification")
            # Step descriptions for roleplay
            steps = [
            "Step 1 of 6: before you write a response to the user's text, what is your understanding of theory of mind."
            ]

            classification = "this is a text classification request. please classify whether the text is a roleplay of some form. to indicate whether it is or isn't please output 'y' or 'n' without the quotes around the letter. you have only one (1) token to respond with."

            roleplay_classification = self.query_openai_endpoint(prompt = prompt, 
            system_content = classification, 
            max_tokens = 1
            )
            roleplay_classification = self.get_first_character(roleplay_classification)
            print(f"classification: {roleplay_classification}")

            if roleplay_classification == 'y':
                print("entered RP prompting")
                RPGCoT = ""
                for step in steps:
                    RPGCoT += self.roleplay_step(prompt, step, RPGCoT)

                return self.query_openai_endpoint(prompt = prompt, 
                system_content = f"this is an interactive roleplay, please keep to the character that has been established by the text that {self.settings_frame.return_username()} submits.", 
                assistant_content = RPGCoT
                )
        # This method call uses keyword arguments to explicitly specify which values correspond to which parameters.The 'query_openai_endpoint' method has optional parameters 'assistant_content' and 'max_tokens'. By using keyword arguments, we can set 'prompt' and 'system_content', and optionally 'assistant_content', while leaving 'max_tokens' to default to None. This ensures clarity and avoids confusion with parameter order. more involved explanation: https://chatgpt.com/share/fa5a50b7-19f6-43f2-b499-5999d0c8e485

        else:
            return self.query_openai_endpoint(prompt, "this is a text completion request, please complete it in keeping with the text that the user submits.")


def main():
    system_prompt = "System: You are a helpful AI system called Lux Stellarum that answers questions honestly and truthfully."
    prompt = "Querant: What is a blue bird?"
    completion_prompt = "System: You are a helpful AI system called Lux Stellarum that answers questions honestly and truthfully. \n\nQuerant: What is a blue bird? \n\nResponse: "
    response = query_openai_endpoint_chat_completion(prompt, system_prompt, user_max_tokens, user_temperature, user_top-p)
    #response = query_openai_endpoint_text_completion(completion_prompt, user_max_tokens, user_temperature)
    print(system_prompt)
    print(prompt)
    print("Response from OpenAI endpoint:")
    print(f"response: {response}")

if __name__ == "__main__":
    main()


import openai
from data_handler import DataHandler 
from settings_frame import SettingsFrame

class EndpointConnector:
	def __init__(self, SettingsFrame):
		self.settings_frame = SettingsFrame
        
    def query_openai_endpoint_text_completion_classify(self, prompt):
    client = openai.OpenAI(
        base_url="http://192.168.68.111:6681/v1/", # this will require a variable that takes data from settings_frame.py
        api_key = self.settings_frame.return_api_key()
    )
    
    completion = client.chat.completions.create( 
        model="gpt-3.5-turbo", # this will need a variable passed when this function is called
        messages=[
            {"role": "system", "content": "this is a text classification request. please classify whether the text is a roleplay of some form. to indicate whether it is or isn't please output 'y' or 'n' without the quotes around the letter."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1, 
        temperature=0, 
        frequency_penalty=self.settings_frame.return_freq_pen(),
        presence_penalty=self.settings_frame.return_presence_pen(),
        top_p=self.settings_frame.return_top_P_sampling(),
        user=self.settings_frame.return_username()
    )
    
    print(f"Diagnostics: classifier: {completion.choices[0].message.content}")
    return completion.choices[0].message.content
	
	def query_openai_endpoint_text_completion_response(self, prompt):
    client = openai.OpenAI(
        base_url="http://192.168.68.111:6681/v1/", # this will require a variable that takes data from settings_frame.py
        api_key = self.settings_frame.return_api_key()
    )

    completion = client.chat.completions.create( 
        model="gpt-3.5-turbo", # this will need a variable passed when this function is called
        messages=[
            {"role": "system", "content": "this is a text completion request, please complete it in keeping with the text that the user submits."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=self.settings_frame.return_max_tokens(), 
        temperature=self.settings_frame.return_temp(), 
        frequency_penalty=self.settings_frame.return_freq_pen(),
        presence_penalty=self.settings_frame.return_presence_pen(),
        top_p=self.settings_frame.return_top_P_sampling(),
        user=self.settings_frame.return_username()
    )
    
    print(f"Diagnostics: response: {completion.choices[0].message.content}")
    return completion.choices[0].message.content
    
    def query_openai_endpoint_text_completion_roleplay_thoughts(self, prompt):
    client = openai.OpenAI(
        base_url="http://192.168.68.111:6681/v1/", # this will require a variable that takes data from settings_frame.py
        api_key = self.settings_frame.return_api_key()
    )

    completion = client.chat.completions.create( 
        model="gpt-3.5-turbo", # this will need a variable passed when this function is called
        messages=[
            {"role": "system", "content": "this is a roleplay, you are an AI system taking on the role of a character described by the user. think step by step about the character's motivations, goals and desires. these are the character's inner thoughts and feelings you are writing."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=self.settings_frame.return_max_tokens(), 
        temperature=self.settings_frame.return_temp(), 
        frequency_penalty=self.settings_frame.return_freq_pen(),
        presence_penalty=self.settings_frame.return_presence_pen(),
        top_p=self.settings_frame.return_top_P_sampling(),
        user=self.settings_frame.return_username()
    )
    
    print(f"Diagnostics: roleplay_thoughts: {completion.choices[0].message.content}")
    return completion.choices[0].message.content
    
    def get_response(self, prompt):
    rolplay_question = query_openai_endpoint_text_completion_classify(prompt)
    
    if roleplay_question == y
        RPGCoT = query_openai_endpoint_text_completion_roleplay_thoughts(prompt)
        prompt = prompt + RPGCoT
        return query_openai_endpoint_text_completion_roleplay_thoughts(prompt)
    else
        return query_openai_endpoint_text_completion_response(prompt)


import openai
from data_handler import DataHandler 
#from simple_gui import SettingsFrame

class EndpointConnector:
    def __init__(self, settings_frame):
        self.settings_frame = settings_frame
        
    def query_openai_endpoint_text_completion_classify(self, prompt):
        client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",  # this will require a variable that takes data from settings_frame.py
            api_key=self.settings_frame.return_api_key()
        )
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # this will need a variable passed when this function is called
            messages=[
                {"role": "system", "content": "this is a text classification request. please classify whether the text is a roleplay of some form. to indicate whether it is or isn't please output 'y' or 'n' without the quotes around the letter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1,
            temperature=0.0,
            frequency_penalty=self.settings_frame.return_freq_pen(),
            presence_penalty=self.settings_frame.return_presence_pen(),
            top_p=self.settings_frame.return_top_P_sampling(),
            user=self.settings_frame.return_username()
        )
        
        print(f"Diagnostics: classifier: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
    
    def query_openai_endpoint_text_completion_response(self, prompt):
        client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",  # this will require a variable that takes data from settings_frame.py
            api_key=self.settings_frame.return_api_key()
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # this will need a variable passed when this function is called
            messages=[
                {"role": "system", "content": "this is a text completion request, please complete it in keeping with the text that the user submits."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.settings_frame.return_max_tokens(),
            temperature=self.settings_frame.return_temp(),
            frequency_penalty=self.settings_frame.return_freq_pen(),
            presence_penalty=self.settings_frame.return_presence_pen(),
            top_p=self.settings_frame.return_top_P_sampling(),
            user=self.settings_frame.return_username()
        )
        
        print(f"Diagnostics: response: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
    
    def query_openai_endpoint_text_completion_roleplay_thoughts(self, prompt):
        client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",  # this will require a variable that takes data from settings_frame.py
            api_key=self.settings_frame.return_api_key()
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # this will need a variable passed when this function is called
            messages=[
                {"role": "system", "content": "plan how the character is going to respond, think step by step about the character's motivations, goals and opinions in relation to the topic at hand."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.settings_frame.return_max_tokens(),
            temperature=self.settings_frame.return_temp(),
            frequency_penalty=self.settings_frame.return_freq_pen(),
            presence_penalty=self.settings_frame.return_presence_pen(),
            top_p=self.settings_frame.return_top_P_sampling(),
            user=self.settings_frame.return_username()
        )
        
        print(f"Diagnostics: roleplay_thoughts: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
    
    def get_response(self, prompt):
        roleplay_question = self.query_openai_endpoint_text_completion_classify(prompt)
        
        if roleplay_question == 'y':
            RPGCoT = self.query_openai_endpoint_text_completion_roleplay_thoughts(prompt)
            prompt = prompt + RPGCoT
            return self.query_openai_endpoint_text_completion_response(prompt)
        else:
            return self.query_openai_endpoint_text_completion_response(prompt)

    #step one: recieve the prompt, perform a hidden chain of thought analysis of what the prompt is requesting.
    #step two: take the output of step one, appending it to the beginning or end (depending on which one results in better results) and write the response.
    #step three: return the response. 
    
    #disadvantage with the above system is that once the response is printed the LLM will lose all understanding of why it wrote that response.


import openai
from data_handler import DataHandler 

class EndpointConnector:
    def __init__(self, settings_frame):
        self.settings_frame = settings_frame

    def initialize_client(self):
        return openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",
            api_key=self.settings_frame.return_api_key()
        )

    def query_openai_endpoint(self, prompt, system_content):
        
        
        client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",  # this will require a variable that takes data from settings_frame.py
            api_key=self.settings_frame.return_api_key()
        )
        try
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            max_tokens= self.settings_frame.return_max_tokens(), #max_tokens takes an integer or a null as input
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
        return completion.choices[0].message.content
    
    def query_openai_endpoint_assistant(self, prompt, system_content, CoT):
        
        client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",  # this will require a variable that takes data from settings_frame.py
            api_key=self.settings_frame.return_api_key()
        )
        try
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "assistant", "content": CoT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.settings_frame.return_max_tokens(),
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
        return completion.choices[0].message.content
    
    def query_openai_endpoint_text_completion_classify(self, prompt):
        system_content = "this is a text classification request. please classify whether the text is a roleplay of some form. to indicate whether it is or isn't please output 'y' or 'n' without the quotes around the letter."
        
        try
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1,
            temperature=0.01,
            frequency_penalty=self.settings_frame.return_freq_pen(),
            presence_penalty=self.settings_frame.return_presence_pen(),
            top_p=self.settings_frame.return_top_P_sampling(),
            user=self.settings_frame.return_username()
        )
        except Exception as e:
            print(f"Error during API call: {e}")
            return None
        
        print(f"Diagnostics: classify: {completion.choices[0].message.content}")
        print(f"tokens generated: {completion.usage.completion_tokens}")
        return completion.choices[0].message.content
    
    def query_openai_endpoint_text_completion_response(self, prompt):
        system_content = "this is a text completion request, please complete it in keeping with the text that the user submits."
        
        returned_prompt = self.query_openai_endpoint(prompt, system_content)
        print(f"Diagnostics: completion: {returned_prompt}")
        return returned_prompt
    
    def query_openai_endpoint_text_completion_roleplay_response(self, prompt, CoT):
        system_content = "this is an interactive roleplay, please keep to the character that has been established by the text that the user/querant submits."
        
        returned_prompt = self.query_openai_endpoint_assistant(prompt, system_content, CoT)
        print(f"Diagnostics: completion: {returned_prompt}")
        return returned_prompt
    
    def roleplay_step_1(self, prompt):
        system_content = "Summarise what the character's immediate thoughts and feelings to the situation are."
        
        returned_prompt = self.query_openai_endpoint(prompt, system_content)
        print(f"Diagnostics: roleplay step 1: {system_content} \n\n\ {returned_prompt}")
        return returned_prompt
    
    def roleplay_step_2(self, prompt, RPGCoT):
        system_content = "Summarise what the character's short-term goals appear to be."
        
        returned_prompt = self.query_openai_endpoint_assistant(prompt, system_content, RPGCoT)
        print(f"Diagnostics: roleplay step 2: {system_content} \n\n\ {returned_prompt}")
        return returned_prompt
    
    def roleplay_step_3(self, prompt, RPGCoT):
        system_content = "Summarise how does the character perceive the other participants."
        
        returned_prompt = self.query_openai_endpoint_assistant(prompt, system_content, RPGCoT)
        print(f"Diagnostics: roleplay step 3: {system_content} \n\n\ {returned_prompt}")
        return returned_prompt
        
    def roleplay_step_4(self, prompt, RPGCoT):
        system_content = "Summarise what the character's long-term motivations and goals are."
        
        returned_prompt = self.query_openai_endpoint_assistant(prompt, system_content, RPGCoT)
        print(f"Diagnostics: roleplay step 4: {system_content} \n\n\ {returned_prompt}")
        return returned_prompt
        
    def roleplay_step_5(self, prompt, RPGCoT):
        system_content = "Summarise what actions the character is considering to achieve these goals."
        
        returned_prompt = self.query_openai_endpoint_assistant(prompt, system_content, RPGCoT)
        print(f"Diagnostics: roleplay step 5: {system_content} \n\n\ {returned_prompt}")
        return returned_prompt
     
    def get_response(self, prompt):
        testing = False
        
        if testing == True:
            roleplay_question = self.query_openai_endpoint_text_completion_classify(prompt) #really needs GBNF type thing for this type of classification.
            
            if roleplay_question == 'y':
                RPGCoT = self.roleplay_step_1(prompt)
                RPGCoT += self.roleplay_step_2(prompt, RPGCoT)                
                RPGCoT += self.roleplay_step_3(prompt, RPGCoT)                
                RPGCoT += self.roleplay_step_4(prompt, RPGCoT)                
                RPGCoT += self.roleplay_step_5(prompt, RPGCoT)                
                return self.query_openai_endpoint_text_completion_roleplay_response(prompt, RPGCoT)
            else:
                return self.query_openai_endpoint_text_completion_response(prompt)
        else:
            return self.query_openai_endpoint_text_completion_response(prompt)
            
 https://chatgpt.com/share/7dc68d4c-f0b0-4454-8827-db71ffed1216

    def query_openai_endpoint_text_completion_roleplay_thoughts(self, prompt):
        system_content = ("Plan how the character is going to respond. Think step by step about the character's motivations, goals, and opinions in relation to the topic at hand. "
                  "Consider the character's past actions and experiences in similar situations, as well as their interactions and relationships with other participants. "
                  "this is an internal monologue.")
        
        returned_prompt = self.query_openai_endpoint(prompt, system_content)
        print(f"Diagnostics: roleplay_thoughts: {returned_prompt}")
        return returned_prompt

    def incremental_roleplay_thoughts(self, prompt): #break this out into five methods.
        steps = [
            "What are the character's immediate thoughts and feelings?",
            "What are the character's short-term goals?",
            "How does the character perceive the other participants?",
            "What are the character's long-term motivations and goals?",
            "What actions is the character considering to achieve these goals?"
        ]

        responses = []

        for step in steps:
            step_prompt = f"{step}\nUser prompt: {prompt}"
            response = self.query_openai_endpoint_text_completion_response(step_prompt)
            responses.append(response)
            prompt += " " + response  # Append the response to the prompt for the next step

        final_response = " ".join(responses)
        return final_response

                #RPGCoT = self.query_openai_endpoint_text_completion_roleplay_thoughts(prompt)
                #prompt = prompt + RPGCoT
                #return self.query_openai_endpoint_text_completion_response(prompt)
                
                #return self.incremental_roleplay_thoughts(prompt)
                
                #RPGCoT = self.incremental_roleplay_thoughts(prompt)
                #prompt = prompt + RPGCoT
                #return self.query_openai_endpoint_text_completion_roleplay_response(prompt)

It's indeed a challenge when models struggle to fully grasp certain concepts or directives, especially in areas like role-playing, where context and depth are crucial. Given this limitation, we can consider alternative approaches to achieve more coherent and detailed responses in role-playing scenarios.

### Alternative Approaches:

1. **Incremental Prompting**:
   - Break down the role-playing task into smaller, more manageable prompts. Instead of asking for an entire plan in one go, guide the model through a series of steps.
   
2. **Structured Templates**:
   - Use a structured template to guide the model’s response. This can help the model focus on specific aspects of the role-playing scenario.
   
3. **Fine-Tuning**:
   - If you have the capability, fine-tuning a model on role-playing specific data can significantly improve its performance in generating contextually rich responses.

4. **Feedback Loops**:
   - Implement a feedback loop where the model’s responses are reviewed and refined iteratively. This can help in generating more accurate and detailed role-playing outputs.

### Example: Incremental Prompting

Instead of asking the model to generate a complete response in one go, break it down into a sequence of prompts:

```python
def incremental_roleplay_thoughts(self, prompt):
    steps = [
        "What are the character's immediate thoughts and feelings?",
        "What are the character's short-term goals?",
        "How does the character perceive the other participants?",
        "What are the character's long-term motivations and goals?",
        "What actions is the character considering to achieve these goals?"
    ]
    
    responses = []
    
    for step in steps:
        step_prompt = f"{step}\nUser prompt: {prompt}"
        response = self.query_openai_endpoint_text_completion_response(step_prompt)
        responses.append(response)
        prompt += " " + response  # Append the response to the prompt for the next step

    final_response = " ".join(responses)
    return final_response
```

### Example: Structured Templates

Create a template to guide the model’s response:

https://chatgpt.com/share/af0b3959-8a9a-4844-a259-b47e645c5053
Yes, batching the roleplay steps (steps 1 through 4) into a single API call could potentially improve speed and efficiency. By reducing the number of individual API calls, you can decrease the overhead associated with each request. This can be particularly beneficial if the API has a significant latency per call.

To implement this, you can modify the `roleplay_step` method to handle multiple steps in one go and adjust the `get_response` method accordingly.

Here's how you could refactor the code to batch the first four steps:

```python
import openai
from data_handler import DataHandler 

class EndpointConnector:
    def __init__(self, settings_frame):
        self.settings_frame = settings_frame
        self.client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",
            api_key=self.settings_frame.return_api_key()
        )

    def query_openai_endpoint(self, prompt, system_content, assistant_content=None):
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]
        
        if assistant_content:
            messages.insert(1, {"role": "assistant", "content": assistant_content})
        
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=self.settings_frame.return_max_tokens(),
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
        return completion.choices[0].message.content

    def roleplay_steps_batch(self, prompt, assistant_content=None):
        steps = [
            "Summarise what the character's immediate thoughts and feelings to the situation are.",
            "Summarise what the character's short-term goals appear to be.",
            "Summarise how the character perceives the other participants.",
            "Summarise what the character's long-term motivations and goals are."
        ]
        
        system_content = "Provide a summary for the following steps in sequence:\n" + "\n".join(steps)
        return self.query_openai_endpoint(prompt, system_content, assistant_content)

    def roleplay_step_5(self, prompt, RPGCoT):
        system_content = "Summarise what actions the character is considering to achieve these goals."
        return self.query_openai_endpoint(prompt, system_content, RPGCoT)

    def get_response(self, prompt):
        testing = False
        
        if testing:
            roleplay_classification = self.query_openai_endpoint(prompt, "this is a text classification request. please classify whether the text is a roleplay of some form. to indicate whether it is or isn't please output 'y' or 'n' without the quotes around the letter.")
            
            if roleplay_classification == 'y':
                RPGCoT = self.roleplay_steps_batch(prompt)
                RPGCoT += self.roleplay_step_5(prompt, RPGCoT)
                
                return self.query_openai_endpoint(prompt, "this is an interactive roleplay, please keep to the character that has been established by the text that the user/querant submits.", RPGCoT)
            else:
                return self.query_openai_endpoint(prompt, "this is a text completion request, please complete it in keeping with the text that the user submits.")
        else:
            return self.query_openai_endpoint(prompt, "this is a text completion request, please complete it in keeping with the text that the user submits.")
```

### Explanation

1. **Batch Processing:** The `roleplay_steps_batch` method constructs a single prompt that includes all four steps in sequence. This reduces the number of API calls from four to one for these steps.

2. **Integration:** The `get_response` method is adjusted to call `roleplay_steps_batch` for the first four steps and then `roleplay_step_5` for the final step.

3. **Efficiency:** By batching the first four steps, you reduce the total number of API calls, potentially improving the speed and reducing the latency.

This should provide a worthwhile speed increase by reducing the number of individual API calls, thus minimizing the overhead associated with each request.
'''

'''
```python
def structured_roleplay_thoughts(self, prompt):
    template = (
        "Character's immediate thoughts and feelings:\n\n"
        "Character's short-term goals:\n\n"
        "Character's perception of other participants:\n\n"
        "Character's long-term motivations and goals:\n\n"
        "Character's planned actions to achieve these goals:\n\n"
    )
    
    structured_prompt = f"{template}\nUser prompt: {prompt}"
    response = self.query_openai_endpoint_text_completion_response(structured_prompt)
    return response
```

### Example: Feedback Loop

Implement a feedback mechanism to refine responses:

```python
def feedback_loop_roleplay_thoughts(self, prompt, iterations=3):
    response = self.query_openai_endpoint_text_completion_response(prompt)
    
    for _ in range(iterations):
        feedback_prompt = f"Refine the character's thoughts and actions based on this feedback:\n\n{response}\n\nUser prompt: {prompt}"
        response = self.query_openai_endpoint_text_completion_response(feedback_prompt)
    
    return response
```

### Final Thoughts

While it's unfortunate that the model struggles with certain prompts, using alternative approaches like incremental prompting, structured templates, or feedback loops can help guide the model to produce more detailed and contextually appropriate responses. These methods leverage the model's strengths and provide additional structure to help it generate better outputs.
'''

'''
# simple_gui.py

import tkinter as tk
from tkinter import font
from data_handler import DataHandler
from context_menu import ContextMenu

class SimpleGUI:
    def __init__(self, root, data_handler):
        self.root = root
        self.data_handler = data_handler

        self.output_text_var = tk.StringVar()
        self.data_handler.set_output_text_var(self.output_text_var)

        self.text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)

        self.outputFrame = tk.Frame(self.root, bg="blue", width=self.data_handler.wideFrame, height=self.data_handler.tallFrame)
        self.inputFrame = tk.Frame(self.root, bg="red", width=self.data_handler.wideFrame, height=self.data_handler.shortFrame)
        self.settingsFrame = tk.Frame(self.root, bg="green", width=self.data_handler.narrowFrame, height=self.data_handler.tallFrame)
        self.buttonFrame = tk.Frame(self.root, bg="yellow", width=self.data_handler.narrowFrame, height=self.data_handler.shortFrame)

        self.setup_frames()
        self.input_frame = InputFrame(self.inputFrame, self.data_handler)
        self.output_frame = OutputFrame(self.outputFrame, self.data_handler)  # Initialize OutputFrame
        self.settings_frame = SettingsFrame(self.settingsFrame, self.data_handler)  # Initialize SettingsFrame
        self.utility_bar = UtilityBar(self.root, self.output_frame.output_text_widget, self.output_text_var)  # Initialize UtilityBar

    def setup_frames(self):
        self.outputFrame.grid(row=0, column=0, sticky='nsew')
        self.inputFrame.grid(row=1, column=0, sticky='nsew')
        self.settingsFrame.grid(row=0, column=1, sticky='nsew')
        self.buttonFrame.grid(row=1, column=1, sticky='nsew')

    def run(self):
        self.root.mainloop()

class InputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.input_text_widget = None
        self.create_input_frame()

    def create_input_frame(self):
        input_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.shortFrame, bg='black')
        input_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        input_canvas.pack_propagate(False)

        text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)
        input_text = tk.Text(input_canvas, bg='#89BCEA', font=text_font, width=self.data_handler.text_width, wrap=tk.WORD)
        input_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.input_text_widget = input_text

        scrollbar = tk.Scrollbar(input_canvas, command=input_text.yview)
        scrollbar.pack(side='right', fill='y')
        input_text.config(yscrollcommand=scrollbar.set)

        context_menu = ContextMenu(input_text)
        input_text.bind("<Button-3>", context_menu.show_menu_input)  # Corrected method name
        input_text.insert(tk.END, "Please type here for automatic formatting")

    def clear_text_widget(self):
        self.input_text_widget.delete("1.0", tk.END)

    def return_text(self):
        return self.input_text_widget.get("1.0", tk.END).strip()

class OutputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.output_text_widget = None
        self.create_output_frame()

    def create_output_frame(self):
        output_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.tallFrame, bg='black')
        output_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)

        text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)
        output_text = tk.Text(output_canvas, bg='#89BCEA', font=text_font, width=self.data_handler.text_width, wrap=tk.WORD)
        output_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.output_text_widget = output_text

        scrollbar = tk.Scrollbar(output_canvas, command=output_text.yview)
        scrollbar.pack(side='right', fill='y')
        output_text.config(yscrollcommand=scrollbar.set)

        context_menu = ContextMenu(output_text)
        output_text.bind("<Button-3>", context_menu.show_menu_output)  # Corrected method name
        output_text.insert(tk.END, "The current chat context will be displayed here in full, you can freely edit this if you prefer. use the continue button to tell the LLM to continue a sentence you or it wrote.", self.data_handler.output_text_var.get())

        self.data_handler.output_text_var.trace("w", self.update_text)

    def update_text(self, *args):
        self.output_text_widget.insert(tk.INSERT, self.data_handler.output_text_var.get() + '\n')

class UtilityBar:
    def __init__(self, window, output_frame, output_text_var):
        self.window = window
        self.output_frame = output_frame
        self.output_text_var = output_text_var
        self.create_menu()

    def save(self):
        try:
            text = self.output_frame.get("1.0", "end-1c")
            file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt")
            if file_path:
                with open(file_path, "w") as file:
                    file.write(text)
                tk.messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while saving: {e}")

    def open_file(self):
        try:
            file_path = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "r") as file:
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

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save)
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

    def print_CoT(self):
        text = self.load_text(os.path.join("education", "chain_of_thought.txt"))
        self.output_text_var.set(text)

    def print_ToT(self):
        text = self.load_text(os.path.join("education", "tree_of_thought.txt"))
        self.output_text_var.set(text)

class SettingsFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.create_settings_frame()

    def create_settings_frame(self):
        self.settings_canvas = tk.Canvas(self.parent, width=self.data_handler.narrowFrame, height=self.data_handler.tallFrame, bg='#E7EAEA')
        self.settings_canvas.pack(side='left', fill='both', expand=True)

        settings_frame = tk.Frame(self.settings_canvas, bg='#E7EAEA') #correct
        scrollbar = tk.Scrollbar(self.parent, command=self.settings_canvas.yview) #correct
        scrollbar.pack(side='right', fill='y') #correct

        self.settings_canvas.configure(yscrollcommand=scrollbar.set) #correct
        self.settings_canvas.create_window((0, 0), window=settings_frame, anchor='nw') #correct
        settings_frame.bind("<Configure>", lambda e: self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox("all"))) #correct, also interesting. if my eyes are reading what is there correctly, that would be code to define a scroll region meaning that when I use the scroll wheel for instance, it will only occur when my cursor is in the region. so that's nice.
        
        tk.Label(settings_frame, text="API mode").pack()
        options = ["OpenAI", "Gemini", "OpenAI compatible Endpoint"]
        self.selected_option = tk.StringVar(settings_frame)
        self.selected_option.set(options[0])
        option_menu = tk.OptionMenu(settings_frame, self.selected_option, *options)
        option_menu.pack()
        self.selected_option.trace("w", self.update_selected_option)

        tk.Label(settings_frame, text="Endpoint to connect to").pack()
        self.endpoint = tk.Entry(settings_frame, bg='#89BCEA')
        self.endpoint.pack()

        tk.Label(settings_frame, text="API key for OpenAI, Gemini, or similar").pack()
        self.api_key = tk.Entry(settings_frame, bg='#89BCEA')
        self.api_key.pack()

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
        self.user_name.pack()

        self.settings_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.settings_canvas.bind_all("<Button-4>", self.on_mouse_wheel)
        self.settings_canvas.bind_all("<Button-5>", self.on_mouse_wheel)

    def update_selected_option(self, *args):
        self.data_handler.set_selected_option(self.selected_option.get())

    def on_mouse_wheel(self, event):
        if event.delta:
            self.parent.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            self.parent.yview_scroll(-1, "units")
        elif event.num == 5:
            self.parent.yview_scroll(1, "units")

    def return_max_tokens(self):
        return self.tokens_entry.get()

    def return_temp(self):
        return self.temperature_scale.get()
        
        
    def save_settings(self):
        font_family = self.font_entry.get()
        font_size = int(self.font_size_entry.get())

        self.data_handler.text_font_family = font_family
        self.data_handler.font_size = font_size

if __name__ == "__main__":
    def main():
        root = tk.Tk()
        data_handler = DataHandler()
        gui = SimpleGUI(root, data_handler)
        gui.run()

    main()

'''

'''
# simple_gui.py

import tkinter as tk
from tkinter import font
from data_handler import DataHandler
from context_menu import ContextMenu
import os

class SimpleGUI:
    def __init__(self, root, data_handler):
        self.root = root
        self.data_handler = data_handler

        self.output_text_var = tk.StringVar()
        self.data_handler.set_output_text_var(self.output_text_var)

        self.text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)

        self.outputFrame = tk.Frame(self.root, bg="blue", width=self.data_handler.wideFrame, height=self.data_handler.tallFrame)
        self.inputFrame = tk.Frame(self.root, bg="red", width=self.data_handler.wideFrame, height=self.data_handler.shortFrame)
        self.settingsFrame = tk.Frame(self.root, bg="green", width=self.data_handler.narrowFrame, height=self.data_handler.tallFrame)
        self.buttonFrame = tk.Frame(self.root, bg="yellow", width=self.data_handler.narrowFrame, height=self.data_handler.shortFrame)

        self.setup_frames()
        self.input_frame = InputFrame(self.inputFrame, self.data_handler)
        self.output_frame = OutputFrame(self.outputFrame, self.data_handler)  # Initialize OutputFrame
        self.utility_bar = UtilityBar(self.root, self.output_frame.output_text_widget, self.output_text_var)  # Initialize UtilityBar

    def setup_frames(self):
        self.outputFrame.grid(row=0, column=0, sticky='nsew')
        self.inputFrame.grid(row=1, column=0, sticky='nsew')
        self.settingsFrame.grid(row=0, column=1, sticky='nsew')
        self.buttonFrame.grid(row=1, column=1, sticky='nsew')

    def run(self):
        self.root.mainloop()

class InputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.input_text_widget = None
        self.create_input_frame()

    def create_input_frame(self):
        input_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.shortFrame, bg='black')
        input_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        input_canvas.pack_propagate(False)

        text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)
        input_text = tk.Text(input_canvas, bg='#89BCEA', font=text_font, width=self.data_handler.text_width, wrap=tk.WORD)
        input_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.input_text_widget = input_text

        scrollbar = tk.Scrollbar(input_canvas, command=input_text.yview)
        scrollbar.pack(side='right', fill='y')
        input_text.config(yscrollcommand=scrollbar.set)

        context_menu = ContextMenu(input_text)
        input_text.bind("<Button-3>", context_menu.show_menu_input)
        input_text.insert(tk.END, "Please type here for automatic formatting")

    def clear_text_widget(self):
        self.input_text_widget.delete("1.0", tk.END)

    def return_text(self):
        return self.input_text_widget.get("1.0", tk.END).strip()

class OutputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.output_text_widget = None
        self.create_output_frame()

    def create_output_frame(self):
        output_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.tallFrame, bg='black')
        output_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)

        text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)
        output_text = tk.Text(output_canvas, bg='#89BCEA', font=text_font, width=self.data_handler.text_width, wrap=tk.WORD)
        output_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.output_text_widget = output_text

        scrollbar = tk.Scrollbar(output_canvas, command=output_text.yview)
        scrollbar.pack(side='right', fill='y')
        output_text.config(yscrollcommand=scrollbar.set)

        context_menu = ContextMenu(output_text)
        output_text.bind("<Button-3>", context_menu.show_menu_output)
        output_text.insert(tk.END, "The current chat context will be displayed here in full, you can freely edit this if you prefer. use the continue button to tell the LLM to continue a sentence you or it wrote.", self.data_handler.output_text_var.get())

        self.data_handler.output_text_var.trace("w", self.update_text)

    def update_text(self, *args):
        self.output_text_widget.insert(tk.INSERT, self.data_handler.output_text_var.get() + '\n')

class UtilityBar:
    def __init__(self, window, output_frame, output_text_var):
        self.window = window
        self.output_frame = output_frame
        self.output_text_var = output_text_var
        self.create_menu()

    def save(self):
        try:
            text = self.output_frame.get("1.0", "end-1c")
            file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt")
            if file_path:
                with open(file_path, "w") as file:
                    file.write(text)
                tk.messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while saving: {e}")

    def open_file(self):
        try:
            file_path = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "r") as file:
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

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save)
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

    def print_CoT(self):
        text = self.load_text(os.path.join("education", "chain_of_thought.txt"))
        self.output_text_var.set(text)

    def print_ToT(self):
        text = self.load_text(os.path.join("education", "tree_of_thought.txt"))
        self.output_text_var.set(text)

if __name__ == "__main__":
    root = tk.Tk()
    data_handler = DataHandler()
    gui = SimpleGUI(root, data_handler)
    gui.run()
'''

'''
# simple_gui.py

import tkinter as tk
from tkinter import font
from data_handler import DataHandler
from context_menu import ContextMenu
import os

class SimpleGUI:
    def __init__(self, root, data_handler):
        self.root = root
        self.data_handler = data_handler

        self.output_text_var = tk.StringVar()
        self.data_handler.set_output_text_var(self.output_text_var)

        self.text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)

        self.outputFrame = tk.Frame(self.root, bg="blue", width=self.data_handler.wideFrame, height=self.data_handler.tallFrame)
        self.inputFrame = tk.Frame(self.root, bg="red", width=self.data_handler.wideFrame, height=self.data_handler.shortFrame)
        self.settingsFrame = tk.Frame(self.root, bg="green", width=self.data_handler.narrowFrame, height=self.data_handler.tallFrame)
        self.buttonFrame = tk.Frame(self.root, bg="yellow", width=self.data_handler.narrowFrame, height=self.data_handler.shortFrame)

        self.setup_frames()
        self.input_frame = InputFrame(self.inputFrame, self.data_handler)
        self.output_frame = OutputFrame(self.outputFrame, self.data_handler)  # Initialize OutputFrame
        self.settings_frame = SettingsFrame(self.settingsFrame, self.data_handler)  # Initialize SettingsFrame
        self.utility_bar = UtilityBar(self.root, self.output_frame.output_text_widget, self.output_text_var)  # Initialize UtilityBar

    def setup_frames(self):
        self.outputFrame.grid(row=0, column=0, sticky='nsew')
        self.inputFrame.grid(row=1, column=0, sticky='nsew')
        self.settingsFrame.grid(row=0, column=1, sticky='nsew')
        self.buttonFrame.grid(row=1, column=1, sticky='nsew')

    def run(self):
        self.root.mainloop()

class SettingsFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.create_settings_frame()

    def create_settings_frame(self):
        self.settings_canvas = tk.Canvas(self.parent, width=self.data_handler.narrowFrame, height=self.data_handler.tallFrame, bg='#E7EAEA')
        self.settings_canvas.pack(side='left', fill='both', expand=True)

        settings_frame = tk.Frame(self.settings_canvas, bg='#E7EAEA')
        scrollbar = tk.Scrollbar(self.parent, command=self.settings_canvas.yview)
        scrollbar.pack(side='right', fill='y')

        self.settings_canvas.configure(yscrollcommand=scrollbar.set)
        self.settings_canvas.create_window((0, 0), window=settings_frame, anchor='nw')
        settings_frame.bind('<Configure>', lambda event: self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox('all')))

        tk.Label(settings_frame, text="API mode").pack()
        options = ["OpenAI", "Gemini", "OpenAI compatible Endpoint"]
        self.selected_option = tk.StringVar(settings_frame)
        self.selected_option.set(options[0])
        option_menu = tk.OptionMenu(settings_frame, self.selected_option, *options)
        option_menu.pack()
        self.selected_option.trace("w", self.update_selected_option)

        tk.Label(settings_frame, text="Endpoint to connect to").pack()
        self.endpoint = tk.Entry(settings_frame, bg='#89BCEA')
        self.endpoint.pack()

        tk.Label(settings_frame, text="API key for OpenAI, Gemini, or similar").pack()
        self.api_key = tk.Entry(settings_frame, bg='#89BCEA')
        self.api_key.pack()

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
        self.user_name.pack()

        self.settings_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.settings_canvas.bind_all("<Button-4>", self.on_mouse_wheel)
        self.settings_canvas.bind_all("<Button-5>", self.on_mouse_wheel)

    def update_selected_option(self, *args):
        self.data_handler.set_selected_option(self.selected_option.get())

    def on_mouse_wheel(self, event):
        if event.delta:
            self.parent.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            self.parent.yview_scroll(-1, "units")
        elif event.num == 5:
            self.parent.yview_scroll(1, "units")

    def return_max_tokens(self):
        return self.tokens_entry.get()

    def return_temp(self):
        return self.temperature_scale.get()

class InputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.input_text_widget = None
        self.create_input_frame()

    def create_input_frame(self):
        input_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.shortFrame, bg='black')
        input_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        input_canvas.pack_propagate(False)

        input_text_frame = tk.Frame(input_canvas, bg='#E7EAEA')
        input_canvas.create_window((0, 0), window=input_text_frame, anchor='nw')

        self.input_text_widget = tk.Text(input_text_frame, wrap='word', font=self.data_handler.text_font)
        self.input_text_widget.pack(expand=True, fill='both')

        context_menu = ContextMenu(self.input_text_widget)
        self.input_text_widget.bind("<Button-3>", context_menu.show_menu_input)

class OutputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.output_text_widget = None
        self.create_output_frame()

    def create_output_frame(self):
        output_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.tallFrame, bg='black')
        output_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        output_canvas.pack_propagate(False)

        output_text_frame = tk.Frame(output_canvas, bg='#E7EAEA')
        output_canvas.create_window((0, 0), window=output_text_frame, anchor='nw')

        self.output_text_widget = tk.Text(output_text_frame, wrap='word', font=self.data_handler.text_font)
        self.output_text_widget.pack(expand=True, fill='both')

        context_menu = ContextMenu(self.output_text_widget)
        self.output_text_widget.bind("<Button-3>", context_menu.show_menu_output)

class UtilityBar:
    def __init__(self, root, output_text_widget, output_text_var):
        self.root = root
        self.output_text_widget = output_text_widget
        self.output_text_var = output_text_var
        self.create_utility_bar()

    def create_utility_bar(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Clear Output", command=self.clear_output)
        filemenu.add_command(label="Save Output", command=self.save_output)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    def clear_output(self):
        self.output_text_widget.delete(1.0, tk.END)
        self.output_text_var.set("")

    def save_output(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.output_text_widget.get(1.0, tk.END))


'''


'''
# simple_gui.py

import tkinter as tk
from tkinter import font
from data_handler import DataHandler
from context_menu import ContextMenu

class SimpleGUI:
    def __init__(self, root, data_handler):
        self.root = root
        self.data_handler = data_handler

        self.output_text_var = tk.StringVar()
        self.data_handler.set_output_text_var(self.output_text_var)

        self.text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)

        self.outputFrame = tk.Frame(self.root, bg="blue", width=self.data_handler.wideFrame, height=self.data_handler.tallFrame)
        self.inputFrame = tk.Frame(self.root, bg="red", width=self.data_handler.wideFrame, height=self.data_handler.shortFrame)
        self.settingsFrame = tk.Frame(self.root, bg="green", width=self.data_handler.narrowFrame, height=self.data_handler.tallFrame)
        self.buttonFrame = tk.Frame(self.root, bg="yellow", width=self.data_handler.narrowFrame, height=self.data_handler.shortFrame)

        self.setup_frames()
        self.input_frame = InputFrame(self.inputFrame, self.data_handler)
        self.output_frame = OutputFrame(self.outputFrame, self.data_handler)  # Initialize OutputFrame

    def setup_frames(self):
        self.outputFrame.grid(row=0, column=0, sticky='nsew')
        self.inputFrame.grid(row=1, column=0, sticky='nsew')
        self.settingsFrame.grid(row=0, column=1, sticky='nsew')
        self.buttonFrame.grid(row=1, column=1, sticky='nsew')

    def run(self):
        self.root.mainloop()

class InputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.input_text_widget = None
        self.create_input_frame()

    def create_input_frame(self):
        input_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.shortFrame, bg='black')
        input_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        input_canvas.pack_propagate(False)

        text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)
        input_text = tk.Text(input_canvas, bg='#89BCEA', font=text_font, width=self.data_handler.text_width, wrap=tk.WORD)
        input_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.input_text_widget = input_text

        scrollbar = tk.Scrollbar(input_canvas, command=input_text.yview)
        scrollbar.pack(side='right', fill='y')
        input_text.config(yscrollcommand=scrollbar.set)

        context_menu = ContextMenu(input_text)
        input_text.bind("<Button-3>", context_menu.show_menu_input)
        input_text.insert(tk.END, "Please type here for automatic formatting")

    def clear_text_widget(self):
        self.input_text_widget.delete("1.0", tk.END)

    def return_text(self):
        return self.input_text_widget.get("1.0", tk.END).strip()

class OutputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.output_text_widget = None
        self.create_output_frame()

    def create_output_frame(self):
        output_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.tallFrame, bg='black')
        output_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)

        text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)
        output_text = tk.Text(output_canvas, bg='#89BCEA', font=text_font, width=self.data_handler.text_width, wrap=tk.WORD)
        output_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.output_text_widget = output_text

        scrollbar = tk.Scrollbar(output_canvas, command=output_text.yview)
        scrollbar.pack(side='right', fill='y')
        output_text.config(yscrollcommand=scrollbar.set)

        context_menu = ContextMenu(output_text)
        output_text.bind("<Button-3>", context_menu.show_menu_output)
        output_text.insert(tk.END, "The current chat context will be displayed here in full, you can freely edit this if you prefer. use the continue button to tell the LLM to continue a sentence you or it wrote.", self.data_handler.output_text_var.get())

        self.data_handler.output_text_var.trace("w", self.update_text)

    def update_text(self, *args):
        self.output_text_widget.insert(tk.INSERT, self.data_handler.output_text_var.get() + '\n')
'''


'''
# simple_gui.py

import tkinter as tk
from tkinter import font
from data_handler import DataHandler
from context_menu import ContextMenu

class SimpleGUI:
    def __init__(self, root, data_handler):
        self.root = root
        self.data_handler = data_handler

        self.output_text_var = tk.StringVar()
        self.data_handler.set_output_text_var(self.output_text_var)

        self.text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)

        self.outputFrame = tk.Frame(self.root, bg="blue", width=self.data_handler.wideFrame, height=self.data_handler.tallFrame)
        self.inputFrame = tk.Frame(self.root, bg="red", width=self.data_handler.wideFrame, height=self.data_handler.shortFrame)
        self.settingsFrame = tk.Frame(self.root, bg="green", width=self.data_handler.narrowFrame, height=self.data_handler.tallFrame)
        self.buttonFrame = tk.Frame(self.root, bg="yellow", width=self.data_handler.narrowFrame, height=self.data_handler.shortFrame)

        self.setup_frames()
        self.input_frame = InputFrame(self.inputFrame, self.data_handler)  # Initialize InputFrame

    def setup_frames(self):
        self.outputFrame.grid(row=0, column=0, sticky='nsew')
        self.inputFrame.grid(row=1, column=0, sticky='nsew')
        self.settingsFrame.grid(row=0, column=1, sticky='nsew')
        self.buttonFrame.grid(row=1, column=1, sticky='nsew')

    def run(self):
        self.root.mainloop()

class InputFrame:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.input_text_widget = None
        self.create_input_frame()

    def create_input_frame(self):
        input_canvas = tk.Canvas(self.parent, width=self.data_handler.wideFrame, height=self.data_handler.shortFrame, bg='black')
        input_canvas.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        input_canvas.pack_propagate(False)

        text_font = font.Font(family=self.data_handler.text_font_family, size=self.data_handler.font_size)
        input_text = tk.Text(input_canvas, bg='#89BCEA', font=text_font, width=self.data_handler.text_width, wrap=tk.WORD)
        input_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.input_text_widget = input_text  # Store the input text widget as an instance variable

        scrollbar = tk.Scrollbar(input_canvas, command=input_text.yview)
        scrollbar.pack(side='right', fill='y')
        input_text.config(yscrollcommand=scrollbar.set)
        
        context_menu = ContextMenu(input_text)
        input_text.bind("<Button-3>", context_menu.show_menu_input)
        input_text.insert(tk.END, "Please type here for automatic formatting")

    def clear_text_widget(self):
        self.input_text_widget.delete("1.0", tk.END)

    def return_text(self):
        return self.input_text_widget.get("1.0", tk.END).strip()

'''

'''
to create the GUI in full I will need to give GPT-4o this module, the data_handler module and the relevant frame's module and ask it to convert the frame module into relevant classes that would be added to simple_gui and data_handler respectively.
'''

'''
import openai
from data_handler import DataHandler 

def query_openai_endpoint_text_completion_class_input(prompt, settings_frame):
    client = openai.OpenAI(
        base_url="http://192.168.68.111:6681/v1/", # this will require a variable that takes data from settings_frame.py
        api_key = settings_frame.return_api_key()
    )

    completion = client.chat.completions.create( 
        model="gpt-3.5-turbo", # this will need a variable passed when this function is called
        messages=[
            {"role": "system", "content": "this is a text completion request, please complete it in keeping with the text that the user submits."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=settings_frame.return_max_tokens(), 
        temperature=settings_frame.return_temp(), 
        frequency_penalty=settings_frame.return_freq_pen(),
        presence_penalty=settings_frame.return_presence_pen(),
        top_p=settings_frame.return_top_P_sampling(),
        user=settings_frame.return_username()
    )
    
    print(f"Diagnostics: response: {completion.choices[0].message.content}")
    return completion.choices[0].message.content


def main():
    system_prompt = "System: You are a helpful AI system called Lux Stellarum that answers questions honestly and truthfully."
    prompt = "Querant: What is a blue bird?"
    completion_prompt = "System: You are a helpful AI system called Lux Stellarum that answers questions honestly and truthfully. \n\nQuerant: What is a blue bird? \n\nResponse: "
    response = query_openai_endpoint_chat_completion(prompt, system_prompt, user_max_tokens, user_temperature, user_top-p)
    #response = query_openai_endpoint_text_completion(completion_prompt, user_max_tokens, user_temperature)
    print(system_prompt)
    print(prompt)
    print("Response from OpenAI endpoint:")
    print(f"response: {response}")

if __name__ == "__main__":
    main()


import openai
from data_handler import DataHandler 
from settings_frame import SettingsFrame

class EndpointConnector:
	def __init__(self, SettingsFrame):
		self.settings_frame = SettingsFrame
        
    def query_openai_endpoint_text_completion_classify(self, prompt):
    client = openai.OpenAI(
        base_url="http://192.168.68.111:6681/v1/", # this will require a variable that takes data from settings_frame.py
        api_key = self.settings_frame.return_api_key()
    )
    
    completion = client.chat.completions.create( 
        model="gpt-3.5-turbo", # this will need a variable passed when this function is called
        messages=[
            {"role": "system", "content": "this is a text classification request. please classify whether the text is a roleplay of some form. to indicate whether it is or isn't please output 'y' or 'n' without the quotes around the letter."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1, 
        temperature=0, 
        frequency_penalty=self.settings_frame.return_freq_pen(),
        presence_penalty=self.settings_frame.return_presence_pen(),
        top_p=self.settings_frame.return_top_P_sampling(),
        user=self.settings_frame.return_username()
    )
    
    print(f"Diagnostics: classifier: {completion.choices[0].message.content}")
    return completion.choices[0].message.content
	
	def query_openai_endpoint_text_completion_response(self, prompt):
    client = openai.OpenAI(
        base_url="http://192.168.68.111:6681/v1/", # this will require a variable that takes data from settings_frame.py
        api_key = self.settings_frame.return_api_key()
    )

    completion = client.chat.completions.create( 
        model="gpt-3.5-turbo", # this will need a variable passed when this function is called
        messages=[
            {"role": "system", "content": "this is a text completion request, please complete it in keeping with the text that the user submits."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=self.settings_frame.return_max_tokens(), 
        temperature=self.settings_frame.return_temp(), 
        frequency_penalty=self.settings_frame.return_freq_pen(),
        presence_penalty=self.settings_frame.return_presence_pen(),
        top_p=self.settings_frame.return_top_P_sampling(),
        user=self.settings_frame.return_username()
    )
    
    print(f"Diagnostics: response: {completion.choices[0].message.content}")
    return completion.choices[0].message.content
    
    def query_openai_endpoint_text_completion_roleplay_thoughts(self, prompt):
    client = openai.OpenAI(
        base_url="http://192.168.68.111:6681/v1/", # this will require a variable that takes data from settings_frame.py
        api_key = self.settings_frame.return_api_key()
    )

    completion = client.chat.completions.create( 
        model="gpt-3.5-turbo", # this will need a variable passed when this function is called
        messages=[
            {"role": "system", "content": "this is a roleplay, you are an AI system taking on the role of a character described by the user. think step by step about the character's motivations, goals and desires. these are the character's inner thoughts and feelings you are writing."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=self.settings_frame.return_max_tokens(), 
        temperature=self.settings_frame.return_temp(), 
        frequency_penalty=self.settings_frame.return_freq_pen(),
        presence_penalty=self.settings_frame.return_presence_pen(),
        top_p=self.settings_frame.return_top_P_sampling(),
        user=self.settings_frame.return_username()
    )
    
    print(f"Diagnostics: roleplay_thoughts: {completion.choices[0].message.content}")
    return completion.choices[0].message.content
    
    def get_response(self, prompt):
    rolplay_question = query_openai_endpoint_text_completion_classify(prompt)
    
    if roleplay_question == y
        RPGCoT = query_openai_endpoint_text_completion_roleplay_thoughts(prompt)
        prompt = prompt + RPGCoT
        return query_openai_endpoint_text_completion_roleplay_thoughts(prompt)
    else
        return query_openai_endpoint_text_completion_response(prompt)


import openai
from data_handler import DataHandler 
#from simple_gui import SettingsFrame

class EndpointConnector:
    def __init__(self, settings_frame):
        self.settings_frame = settings_frame
        
    def query_openai_endpoint_text_completion_classify(self, prompt):
        client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",  # this will require a variable that takes data from settings_frame.py
            api_key=self.settings_frame.return_api_key()
        )
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # this will need a variable passed when this function is called
            messages=[
                {"role": "system", "content": "this is a text classification request. please classify whether the text is a roleplay of some form. to indicate whether it is or isn't please output 'y' or 'n' without the quotes around the letter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1,
            temperature=0.0,
            frequency_penalty=self.settings_frame.return_freq_pen(),
            presence_penalty=self.settings_frame.return_presence_pen(),
            top_p=self.settings_frame.return_top_P_sampling(),
            user=self.settings_frame.return_username()
        )
        
        print(f"Diagnostics: classifier: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
    
    def query_openai_endpoint_text_completion_response(self, prompt):
        client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",  # this will require a variable that takes data from settings_frame.py
            api_key=self.settings_frame.return_api_key()
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # this will need a variable passed when this function is called
            messages=[
                {"role": "system", "content": "this is a text completion request, please complete it in keeping with the text that the user submits."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.settings_frame.return_max_tokens(),
            temperature=self.settings_frame.return_temp(),
            frequency_penalty=self.settings_frame.return_freq_pen(),
            presence_penalty=self.settings_frame.return_presence_pen(),
            top_p=self.settings_frame.return_top_P_sampling(),
            user=self.settings_frame.return_username()
        )
        
        print(f"Diagnostics: response: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
    
    def query_openai_endpoint_text_completion_roleplay_thoughts(self, prompt):
        client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",  # this will require a variable that takes data from settings_frame.py
            api_key=self.settings_frame.return_api_key()
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # this will need a variable passed when this function is called
            messages=[
                {"role": "system", "content": "plan how the character is going to respond, think step by step about the character's motivations, goals and opinions in relation to the topic at hand."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.settings_frame.return_max_tokens(),
            temperature=self.settings_frame.return_temp(),
            frequency_penalty=self.settings_frame.return_freq_pen(),
            presence_penalty=self.settings_frame.return_presence_pen(),
            top_p=self.settings_frame.return_top_P_sampling(),
            user=self.settings_frame.return_username()
        )
        
        print(f"Diagnostics: roleplay_thoughts: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
    
    def get_response(self, prompt):
        roleplay_question = self.query_openai_endpoint_text_completion_classify(prompt)
        
        if roleplay_question == 'y':
            RPGCoT = self.query_openai_endpoint_text_completion_roleplay_thoughts(prompt)
            prompt = prompt + RPGCoT
            return self.query_openai_endpoint_text_completion_response(prompt)
        else:
            return self.query_openai_endpoint_text_completion_response(prompt)

    #step one: recieve the prompt, perform a hidden chain of thought analysis of what the prompt is requesting.
    #step two: take the output of step one, appending it to the beginning or end (depending on which one results in better results) and write the response.
    #step three: return the response. 
    
    #disadvantage with the above system is that once the response is printed the LLM will lose all understanding of why it wrote that response.


import openai
from data_handler import DataHandler 

class EndpointConnector:
    def __init__(self, settings_frame):
        self.settings_frame = settings_frame

    def initialize_client(self):
        return openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",
            api_key=self.settings_frame.return_api_key()
        )

    def query_openai_endpoint(self, prompt, system_content):
        
        
        client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",  # this will require a variable that takes data from settings_frame.py
            api_key=self.settings_frame.return_api_key()
        )
        try
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            max_tokens= self.settings_frame.return_max_tokens(), #max_tokens takes an integer or a null as input
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
        return completion.choices[0].message.content
    
    def query_openai_endpoint_assistant(self, prompt, system_content, CoT):
        
        client = openai.OpenAI(
            base_url="http://192.168.68.111:6681/v1/",  # this will require a variable that takes data from settings_frame.py
            api_key=self.settings_frame.return_api_key()
        )
        try
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "assistant", "content": CoT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.settings_frame.return_max_tokens(),
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
        return completion.choices[0].message.content
    
    def query_openai_endpoint_text_completion_classify(self, prompt):
        system_content = "this is a text classification request. please classify whether the text is a roleplay of some form. to indicate whether it is or isn't please output 'y' or 'n' without the quotes around the letter."
        
        try
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1,
            temperature=0.01,
            frequency_penalty=self.settings_frame.return_freq_pen(),
            presence_penalty=self.settings_frame.return_presence_pen(),
            top_p=self.settings_frame.return_top_P_sampling(),
            user=self.settings_frame.return_username()
        )
        except Exception as e:
            print(f"Error during API call: {e}")
            return None
        
        print(f"Diagnostics: classify: {completion.choices[0].message.content}")
        print(f"tokens generated: {completion.usage.completion_tokens}")
        return completion.choices[0].message.content
    
    def query_openai_endpoint_text_completion_response(self, prompt):
        system_content = "this is a text completion request, please complete it in keeping with the text that the user submits."
        
        returned_prompt = self.query_openai_endpoint(prompt, system_content)
        print(f"Diagnostics: completion: {returned_prompt}")
        return returned_prompt
    
    def query_openai_endpoint_text_completion_roleplay_response(self, prompt, CoT):
        system_content = "this is an interactive roleplay, please keep to the character that has been established by the text that the user/querant submits."
        
        returned_prompt = self.query_openai_endpoint_assistant(prompt, system_content, CoT)
        print(f"Diagnostics: completion: {returned_prompt}")
        return returned_prompt
    
    def roleplay_step_1(self, prompt):
        system_content = "Summarise what the character's immediate thoughts and feelings to the situation are."
        
        returned_prompt = self.query_openai_endpoint(prompt, system_content)
        print(f"Diagnostics: roleplay step 1: {system_content} \n\n\ {returned_prompt}")
        return returned_prompt
    
    def roleplay_step_2(self, prompt, RPGCoT):
        system_content = "Summarise what the character's short-term goals appear to be."
        
        returned_prompt = self.query_openai_endpoint_assistant(prompt, system_content, RPGCoT)
        print(f"Diagnostics: roleplay step 2: {system_content} \n\n\ {returned_prompt}")
        return returned_prompt
    
    def roleplay_step_3(self, prompt, RPGCoT):
        system_content = "Summarise how does the character perceive the other participants."
        
        returned_prompt = self.query_openai_endpoint_assistant(prompt, system_content, RPGCoT)
        print(f"Diagnostics: roleplay step 3: {system_content} \n\n\ {returned_prompt}")
        return returned_prompt
        
    def roleplay_step_4(self, prompt, RPGCoT):
        system_content = "Summarise what the character's long-term motivations and goals are."
        
        returned_prompt = self.query_openai_endpoint_assistant(prompt, system_content, RPGCoT)
        print(f"Diagnostics: roleplay step 4: {system_content} \n\n\ {returned_prompt}")
        return returned_prompt
        
    def roleplay_step_5(self, prompt, RPGCoT):
        system_content = "Summarise what actions the character is considering to achieve these goals."
        
        returned_prompt = self.query_openai_endpoint_assistant(prompt, system_content, RPGCoT)
        print(f"Diagnostics: roleplay step 5: {system_content} \n\n\ {returned_prompt}")
        return returned_prompt
     
    def get_response(self, prompt):
        testing = False
        
        if testing == True:
            roleplay_question = self.query_openai_endpoint_text_completion_classify(prompt) #really needs GBNF type thing for this type of classification.
            
            if roleplay_question == 'y':
                RPGCoT = self.roleplay_step_1(prompt)
                RPGCoT += self.roleplay_step_2(prompt, RPGCoT)                
                RPGCoT += self.roleplay_step_3(prompt, RPGCoT)                
                RPGCoT += self.roleplay_step_4(prompt, RPGCoT)                
                RPGCoT += self.roleplay_step_5(prompt, RPGCoT)                
                return self.query_openai_endpoint_text_completion_roleplay_response(prompt, RPGCoT)
            else:
                return self.query_openai_endpoint_text_completion_response(prompt)
        else:
            return self.query_openai_endpoint_text_completion_response(prompt)
            
 https://chatgpt.com/share/7dc68d4c-f0b0-4454-8827-db71ffed1216

    def query_openai_endpoint_text_completion_roleplay_thoughts(self, prompt):
        system_content = ("Plan how the character is going to respond. Think step by step about the character's motivations, goals, and opinions in relation to the topic at hand. "
                  "Consider the character's past actions and experiences in similar situations, as well as their interactions and relationships with other participants. "
                  "this is an internal monologue.")
        
        returned_prompt = self.query_openai_endpoint(prompt, system_content)
        print(f"Diagnostics: roleplay_thoughts: {returned_prompt}")
        return returned_prompt

    def incremental_roleplay_thoughts(self, prompt): #break this out into five methods.
        steps = [
            "What are the character's immediate thoughts and feelings?",
            "What are the character's short-term goals?",
            "How does the character perceive the other participants?",
            "What are the character's long-term motivations and goals?",
            "What actions is the character considering to achieve these goals?"
        ]

        responses = []

        for step in steps:
            step_prompt = f"{step}\nUser prompt: {prompt}"
            response = self.query_openai_endpoint_text_completion_response(step_prompt)
            responses.append(response)
            prompt += " " + response  # Append the response to the prompt for the next step

        final_response = " ".join(responses)
        return final_response

                #RPGCoT = self.query_openai_endpoint_text_completion_roleplay_thoughts(prompt)
                #prompt = prompt + RPGCoT
                #return self.query_openai_endpoint_text_completion_response(prompt)
                
                #return self.incremental_roleplay_thoughts(prompt)
                
                #RPGCoT = self.incremental_roleplay_thoughts(prompt)
                #prompt = prompt + RPGCoT
                #return self.query_openai_endpoint_text_completion_roleplay_response(prompt)

It's indeed a challenge when models struggle to fully grasp certain concepts or directives, especially in areas like role-playing, where context and depth are crucial. Given this limitation, we can consider alternative approaches to achieve more coherent and detailed responses in role-playing scenarios.

### Alternative Approaches:

1. **Incremental Prompting**:
   - Break down the role-playing task into smaller, more manageable prompts. Instead of asking for an entire plan in one go, guide the model through a series of steps.
   
2. **Structured Templates**:
   - Use a structured template to guide the model’s response. This can help the model focus on specific aspects of the role-playing scenario.
   
3. **Fine-Tuning**:
   - If you have the capability, fine-tuning a model on role-playing specific data can significantly improve its performance in generating contextually rich responses.

4. **Feedback Loops**:
   - Implement a feedback loop where the model’s responses are reviewed and refined iteratively. This can help in generating more accurate and detailed role-playing outputs.

### Example: Incremental Prompting

Instead of asking the model to generate a complete response in one go, break it down into a sequence of prompts:

```python
def incremental_roleplay_thoughts(self, prompt):
    steps = [
        "What are the character's immediate thoughts and feelings?",
        "What are the character's short-term goals?",
        "How does the character perceive the other participants?",
        "What are the character's long-term motivations and goals?",
        "What actions is the character considering to achieve these goals?"
    ]
    
    responses = []
    
    for step in steps:
        step_prompt = f"{step}\nUser prompt: {prompt}"
        response = self.query_openai_endpoint_text_completion_response(step_prompt)
        responses.append(response)
        prompt += " " + response  # Append the response to the prompt for the next step

    final_response = " ".join(responses)
    return final_response
```

### Example: Structured Templates

Create a template to guide the model’s response:

```python
def structured_roleplay_thoughts(self, prompt):
    template = (
        "Character's immediate thoughts and feelings:\n\n"
        "Character's short-term goals:\n\n"
        "Character's perception of other participants:\n\n"
        "Character's long-term motivations and goals:\n\n"
        "Character's planned actions to achieve these goals:\n\n"
    )
    
    structured_prompt = f"{template}\nUser prompt: {prompt}"
    response = self.query_openai_endpoint_text_completion_response(structured_prompt)
    return response
```

### Example: Feedback Loop

Implement a feedback mechanism to refine responses:

```python
def feedback_loop_roleplay_thoughts(self, prompt, iterations=3):
    response = self.query_openai_endpoint_text_completion_response(prompt)
    
    for _ in range(iterations):
        feedback_prompt = f"Refine the character's thoughts and actions based on this feedback:\n\n{response}\n\nUser prompt: {prompt}"
        response = self.query_openai_endpoint_text_completion_response(feedback_prompt)
    
    return response
```

### Final Thoughts

While it's unfortunate that the model struggles with certain prompts, using alternative approaches like incremental prompting, structured templates, or feedback loops can help guide the model to produce more detailed and contextually appropriate responses. These methods leverage the model's strengths and provide additional structure to help it generate better outputs.
'''

'''
# data_handler.py

class DataHandler:
    def __init__(self):
        self.output_text_var = None
        self.text_font_family = "Times New Roman"
        self.font_size = 16
        self.wideFrame = 780
        self.narrowFrame = 210
        self.tallFrame = 455
        self.shortFrame = 195
        
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

    def set_output_text_var(self, output_text_var):
        self.output_text_var = output_text_var

    @property
    def text_width(self):
        return self.wideFrame // self.font_size

    @property
    def text_font(self):
        return (self.text_font_family, self.font_size)
        
    # Getters and setters for settings variables
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
'''


'''
# data_handler.py

# Add similar getters and setters for other variables if needed

class DataHandler:
    def __init__(self):
        self.output_text_var = None
        self.text_font_family = "Times New Roman"
        self.font_size = 16
        self.wideFrame = 780
        self.narrowFrame = 210
        self.tallFrame = 455
        self.shortFrame = 195

    def set_output_text_var(self, output_text_var):
        self.output_text_var = output_text_var

    @property
    def text_width(self):
        return self.wideFrame // self.font_size

    @property
    def text_font(self):
        return (self.text_font_family, self.font_size)
'''