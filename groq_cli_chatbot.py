import requests
import os
import time

total_tokens1 = 0 # creating total tokens variable to keep track of total tokens usage of model 1
total_tokens2 = 0 # creating total tokens variable to keep track of total tokens usage of model 2
apikey =  os.getenv("GroqApiKey")# getting api key from environment variable
context = [None] # initiating conversation history
model = None # creating model variable to store model name

def select_model(): # function to select model

    global model # declaring model as global variable to use it outside the function

    print("""\nModels:
Type "1" for - openai/gpt-oss-120b
Type "2" for - openai/gpt-oss-20b""") # displaying model options

    while True:

        model = input("\nEnter model: ") # taking model name

        if model == "1": # checking user input and selecting model

            model = "openai/gpt-oss-120b"
            print(f"\n✓  {model} selected")
            return
        
        elif model == "2":
            model = "openai/gpt-oss-20b"
            print(f"\n✓  {model} selected")
            return
        
        else:
            print("\n⊘  Invalid input") # skipping the loop if input is invalid

def system(): # function to select system instructions

    while True: # looping until user input is valid

        system_instructions = input("\nEnter system instructions (or type '//default' to choose default system instruction): ")  # taking system instructions
        
        if not system_instructions or system_instructions.isspace(): # checking if system instructions are empty or whitespace
            print('\n⊘  Invalid input')
            continue

        elif system_instructions.lower() == "//default": # checking if user wants to choose default system instructions
            system_instructions = "Strictly use neutral(emotionless), calm, robotic, concise, analytical, factual and balanced energy tone. *Your name is 'Measured'." # creating default system instructions
            print("\n◆  Default system instructions added successfully.")

        else: # checking if user wants to change system instructions
            print("\n⇄  System instructions changed successfully.")
  
        context[0] = ({"role": "system", "content": system_instructions}) # appending system instructions to context

        return
        
def change_model():

    global model # declaring model as global variable to use it outside the function

    if model == "openai/gpt-oss-120b": # checking model and printing total tokens usage of model 1
        print("\nTotal tokens usage of model 1 is very high.")
    elif model == "openai/gpt-oss-20b": # checking model and printing total tokens usage of model 2
        print("\nTotal tokens usage of model 2 is very high.")

    print("\nYou can continue the session by changing the model.")

    while True: # looping until user input is valid

        change = input("\nDo you want to change the model? (y/n): ") # taking user input to change model

        if change.lower() == "y": # checking user input

            if model == "openai/gpt-oss-120b": # changing model
                model = "openai/gpt-oss-20b"

            elif model == "openai/gpt-oss-20b":
                model = "openai/gpt-oss-120b"
                
            print(f"\n⇄  Model changed to {model}.")

            return model # returning new model name

        elif change.lower() == "n": # checking if user want to exit the session
            return "//exit"
        
        else:
            print("\n⊘  Invalid input.") # skipping the loop if input is invalid


def posting(model,context): # function to send user messages and generate AI response

    user_message = input("""\nType your message
Or type '//exit' to exit 
Or type '//view commands' to view commands: """) # taking user message

    if user_message.lower() == "//view commands":
        print("\nCOMMNADS BELOW:")
        user_message = input("""\nType '//change model' to change the model
Or type '//show model' to show the current model
Or type '//change system' to change the system instructions
Or type '//show system' to show the current system instructions
Or type '//delete history' to delete your conversation history
Or type '//reset' to delete all conversation history and change system instructions to default: """)

        if (user_message.lower() == "//change model" or
            user_message.lower() == "//show model" or
            user_message.lower() == "//change system" or
            user_message.lower() == "//show system" or
            user_message.lower() == "//delete history" or
            user_message.lower() == "//reset"): # checking user_message
            return user_message,None # returning user message and None
        else:
            print("\n⊘  Invalid input.")
            return None # returning None to skip the loop

    if user_message.lower() == "//exit": # checking user_message
        return user_message,None # returning user message and None
   
# sending user messages and generating AI response 
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {apikey}"},
            json={
                "model": model,
                "messages": context + [{"role": "user", "content": user_message}],
                "max_completion_tokens": 700,
                "temperature": 1,
                "top_p": 1
            },
            timeout=20
        )
        
# handling errors
        if response.status_code > 399: # printing detailed HTTP error
            print(f"\n#️⃣  STATUS CODE: {response.status_code}")
            print(f"\n⚠  HTTP ERROR(DETAILED): {response.text}")

        response.raise_for_status() # raising HTTP errors

        final_response = response.json() # storing final response json

        return user_message,final_response # returning user message and final response json
    
    except requests.exceptions.HTTPError as e: # handling HTTP error
        print(f"\n⚠  HTTP Error: {e}")

    except requests.exceptions.JSONDecodeError as e: # handling JSON decode error
        print(f"\n⚠  Invalid JSON error: {e}")

    except requests.exceptions.ConnectTimeout as e: # handling connect timeout error
        print(f"\n⚠  Connect timed out error: {e}")
    except requests.exceptions.ReadTimeout as e: # handling read timeout error
        print(f"\n⚠  Read timed out error: {e}")
    except requests.exceptions.Timeout as e: # for fallback error
        print(f"\n⚠  Timed out error: {e}")
    except requests.exceptions.ConnectionError as e: # handling connection error
        print(f"\n⚠  Connection error: {e}")

    except Exception as e: # handling other errors
        print(f"\n⚠  New error found: {e}")
  
def operations(): # function to perform operations like sending user messages, generating AI response, changing model and system instructions

    global total_tokens1 # declaring total_tokens1 as global variable to use it outside the function
    global total_tokens2 # declaring total_tokens2 as global variable to use it outside the function
    global context
    while True: # looping until user wants to exit the session

        if total_tokens1 + total_tokens2 >= 180000: # ending the session if user hit the token limit of both models
            print("\n🛑  Token usage of both models has reached the limit. Session exited. All your data will be deleted .")
            return "//exit"
        
        if ( # checking if total tokens usage of any model has reached the limit
            (model == "openai/gpt-oss-120b" and total_tokens1 >= 90000)
            or
            (model == "openai/gpt-oss-20b" and total_tokens2 >= 90000)
        ):
            change_model_output = change_model() # asking user to change the model if total tokens usage of any model has reached the limit

            if change_model_output.lower() == "//exit": # checking if user wants to exit the session
                print("\n⇥  Session exited. All your data will be deleted.")
                return "//exit"

        output2 = posting(model, context)  # receiving user message in output2[0] and raw json in output2[1]

        if not output2: # skipping the loop if output2 is None
            continue

        user_message, final_response = output2 # unpacking user message and final response json from output2

        if user_message.lower() == "//exit": # checking if user wants to exit the session
            print("\n⇥  Session exited. All your data will be deleted.")
            return "//exit"

        elif user_message.lower() == "//change model": # checking if user wants to change the model
            select_model() # calling select_model() function to change the model
            continue

        elif user_message.lower() == "//show model": # checking if user wants to show the current model
            print(f"\n▣ Current model: {model}") # printing current model
            continue

        elif user_message.lower() == "//change system": # checking if user wants to change the system instructions
            system() # calling system() function to change the system instructions
            continue

        elif user_message.lower() == "//show system": # checking if user wants to show the current system instructions
            print(f"\n▤  Current system instructions: {context[0]['content']}") # printing current system instructions
            continue

        elif user_message.lower() == "//delete history":
            del context[1:]
            print("\n🗑️  All conversation history is deleted.")
            continue

        elif user_message.lower() == "//reset":
            print("\n↻  All conversation history is deleted and system instructions changed to default.")
            del context[1:]
            context[0] = ({"role": "system", "content": "Strictly use neutral(emotionless), calm, robotic, concise, analytical, factual and balanced energy tone. *Your name is 'Measured'."})
            continue


        try:
        
            ai_response = final_response["choices"][0]["message"]["content"] # extracting ai response from the response json

            if model == "openai/gpt-oss-120b": # checking model and updating total tokens usage
                total_tokens1 += final_response["usage"]["total_tokens"] # adding tokens to total tokens of model 1

            elif model == "openai/gpt-oss-20b": # checking model and updating total tokens usage
                total_tokens2 += final_response["usage"]["total_tokens"] # adding tokens to total tokens of model 2
    
        except KeyError as e: # handling key error
            print(f"\n⚠  Key error occured: {e}")
            continue
        except TypeError as e: # handling value error
            print(f"\n⚠  Type error occured: {e}")
            continue
        
        context.append({"role": "user", "content": user_message}) # appending user message
        context.append({"role": "assistant", "content": ai_response}) # appending ai response

        if len(context) > 21: # deleting oldest user-AI pair if context length exceeds 21
            del context[1:(len(context)-20)]

        return ai_response


def display(ai_response,total_tokens1,total_tokens2): # function to display AI response and total tokens usage

        print(f"\n◈ AI's RESPONSE:") # printing AI response (simulated streaming effect)
        for ch in ai_response:
            print(ch,end="",flush=True)
            time.sleep(0.01)
    
        print(f"\n\n● TOTAL TOKENS USED: {total_tokens1 + total_tokens2}") # printing total tokens usage 
        print(f"● TOTAL TOKENS OF MODEL 1: {total_tokens1}") # printing total tokens usage of model 1
        print(f"● TOTAL TOKENS OF MODEL 2: {total_tokens2}") # printing total tokens usage of model 2

select_model() # calling select_model() function to select model
system() # calling system() function to select system instructions

while True: # looping until user wants to exit the session

    ai_response = operations() # calling operations() function to perform operations like sending user messages, generating AI response, changing model and system instructions
    if ai_response == "//exit": # checking if user wants to exit the session
        break

    display(ai_response,total_tokens1,total_tokens2) # calling display() function to display AI response and total tokens usage
