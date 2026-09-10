import requests
import os
import time
from dotenv import load_dotenv

load_dotenv("/storage/emulated/0/Documents/Python_files/apikey.env")

apikey = os.getenv("GroqApiKey1")
context = [] # initiating conversation history
TotalTokens = 0
#---------------------------------------------------
print("""Models: 
Type "1" for openai/gpt-oss-120b
Type "2" for openai/gpt-oss-20b""")
model = input("\nChoose model: ") # taking model name

if model == "1":
    model = "openai/gpt-oss-120b"
    print(f"\n{model} selected")
elif model == "2":
    model = "openai/gpt-oss-20b"
    print(f"\n{model} selected.")
else:
    model = "openai/gpt-oss-20b"
    print(f"\nBecause your model input was invalid, system selected {model}.")
#-----------------------------------------------------
system = input("\nEnter system instructions: ") # taking system instructions

if not system or system.isspace():
    system = "Use strictly robotic, neutral(emotionless), calm,concise, analytical, factual and balanced energy tone. *Your name is 'Measured'." # creating default system instructions
    print("\nSystem selected default system instructions.")

context.append({"role": "system", "content": system}) # appending system instructions
#-----------------------------------------------------
while TotalTokens < 100000: # creating conversation loop

    user = input("\nEnter your message: ") # taking user message    
    user_message = {"role": "user","content": user} # storing user message
#-----------------------------------------------------
# sending user messages and generating AI response
    try:
        posting = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers = {"Authorization": f"Bearer {apikey}"},
            json = {
                "model": model,
                "messages": context + [user_message],
                "max_completion_tokens": 700

            },
            timeout=20
        )
#-----------------------------------------------------------  
        if posting.status_code >= 400: # getting detailed HTTP error
            print("Status:", posting.status_code)
            print("Response:", posting.text)

        posting.raise_for_status()# raising HTTP errors

        response = posting.json() 
        ai_response = response["choices"][0]["message"]["content"] # storing AI response

    # Creating conversation history
        context.append(user_message) # appending user message
        context.append({"role": "assistant","content": ai_response}) # appeding AI response
#-----------------------------------------------------------
        TotalTokens += response["usage"]["total_tokens"] # adding tokens
        print("\n")
        for char in ai_response:
            print(char, end='',flush=True)
            time.sleep(0.01) # printing AI response(simulated streaming effect)

        print(f"\nTOTAL TOKENS USED: {TotalTokens}\n") # printing total used tokens
#-----------------------------------------------------------
    except IndexError: # handling invalid index error
        print("Invalid Index.")
    except KeyError: # handling invalid key error
        print("Expected response format wasn't received.")

    except requests.exceptions.HTTPError as e: # handling HTTP errors
        print(f"HTTP Error: {e}")

    except requests.exceptions.JSONDecodeError as e: # handling invalid JSON format error
        print(f"Invalid JSON format: {e}")

    # handling timed out and connection errors
    except requests.exceptions.ConnectTimeout as e:
        print(f"Connection Timed out: {e}")
    except requests.exceptions.ReadTimeout as e:
        print(f"Read Timed out: {e}")
    except requests.exceptions.Timeout as e:# for fallback error handling.
            print(f"Timeout: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")

    except Exception as e: # handling other errors
        print(f"New Error found: {e}")

print("Your limit has reached.")
