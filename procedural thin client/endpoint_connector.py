import openai

def query_openai_endpoint_text_completion(completion_prompt, user_max_tokens, user_temperature):
    #this method doesn't seem to work nicely with it very much ignoring the maximum tokens stipulated
    client = openai.OpenAI(
        base_url="http://192.168.68.111:6681/v1/", # this will require a variable that takes data from settings_frame.py
        api_key = "sk-no-key-required"
    )
    
    completion_response = client.chat.completions.create( #"C:\Users\DFran\OneDrive\Desktop\AI Art Tools\scripts\python learning\Frontend_V1\LLMfrontend\Lib\site-packages\openai\resources\completions.py"
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "this is a text completion request, please complete it in keeping with the text that the user submits."},
            {"role": "user", "content": completion_prompt}
        ],
        max_tokens=user_max_tokens, # need a variable passed in, also need to figure out why this is being ignored.
        temperature=user_temperature, # need a variable passed in
    )
    
    print(f"\n\n {completion_response} \n\n")
    return completion_response.choices[0].message.content

#I theoretically could stuff the whole conversation into a single text completion by going and using 

def query_openai_endpoint_chat_completion(prompt, system_prompt, user_max_tokens, user_temperature):
    client = openai.OpenAI(
        base_url="http://192.168.68.111:6681/v1/", # this will require a variable that takes data from settings_frame.py
        api_key = "sk-no-key-required"
    )

    completion = client.chat.completions.create( #"C:\Users\DFran\OneDrive\Desktop\AI Art Tools\scripts\python learning\Frontend_V1\LLMfrontend\Lib\site-packages\openai\resources\chat\chat.py"
        model="gpt-3.5-turbo", # this will need a variable passed when this function is called
        messages=[
            {"role": "system", "content": "this is a conversation between querant and respondent in which you are respondent. the role of assistant holds the long term memory of the conversation for respondent. the role of user holds the current topic of discussion. the response to the current topic of discussion may rely upon information held within the role of assistant. do not mention of any information stored within the role of system."},
            {"role": "assistant", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=user_max_tokens, # need a variable passed in, also need to figure out why this is being ignored.
        temperature=user_temperature, # need a variable passed in, also top_p=user_top-p,
    )
    
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

'''
model=get_model(), 
messages=[
    {"role": "system", "content": "this is a text completion request, please complete it in keeping with the text that the user submits."},
    {"role": "user", "content": completion_prompt}
],
max_tokens=return_max_tokens_to_predict(),
temperature=return_temperature(),
frequency_penalty=return_frequency_penalty(),
top_p=return_top-P(),
stop=return_stop_tokens(),
user=get_user_name()
'''


