import requests
import os
import time
import pygame
import math
import threading

# =================================creating variables=============================================================

total_tokens1 = 0 # creating total tokens variable to keep track of total tokens usage of model 1
total_tokens2 = 0 # creating total tokens variable to keep track of total tokens usage of model 2
apikey =  os.getenv("GroqApiKey") # getting api key from environment variable
context = [None] # initiating conversation history
model = None # creating model variable to store model name

# -----------------------ai_avatar function variables-------------------------------------------------------------

ai_status = "idle" # changes ai status 
ai_running = True # terminates the main loop

#====================================ai_avatar====================================================================

def ai_avatar():

    global ai_status
    global ai_running

    pygame.init() # initiating pygame

# ------------------------------variables--------------------------------------------------------------

    width = 600
    height = 700
    screen = pygame.display.set_mode((width,height)) # coloring screen
    pygame.display.set_caption("Artificial Intelligent") # setting caption

    # circle variables
    move = 0 # floats circle
    circle_y = height/2 # circle y axis
    circle_x = width/2 # circle x axis
    size = 150 # circle size

    # arc variables
    angle = 0 # inner arc angle
    angle1 = 0 # outer arc angle
    arc_size = size # arc size

    # speed
    fps = 60 # frame rate per second
    clock = pygame.time.Clock()

# ----------------------------------main loop---------------------------------------------------------------------------

    while ai_running: # starting loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("\nExited ai_avatar function")
                ai_running = False

        screen.fill((0,0,0)) # coloring screen

# ---------------------------------drawing circle-----------------------------------------------------------------------   

        color = 0 # circle blue color
        size = 150 # circle size

        for i in range(150): # running loop for creating multiple circles
            pygame.draw.circle(screen,(0,0,color),(circle_x,circle_y),size) # creating multiple decreasing size circles
            color += 1.5 # increasing blue color towards centre of circle
            size -= 1 # decreasing size of circles

# -----------------------------floating circle--------------------------------------------------------------------------

        circle_y = 250 + math.sin(math.radians(move))*25 # floating circle
        move += 1 # floating circle speed

# --------------------------drawing inner and outer arcs respectively arcs-----------------------------------------------

        rect = (circle_x-arc_size-30,circle_y-arc_size-30,360,360) # creating virtual rect for inner arc
        rect1 = (circle_x-arc_size-60,circle_y-arc_size-60,420,420) # creating virtual rect for outer arc
        arc_width = 15 # creating width of both arcs
        arc_color = 100 # creating blue color of both arcs

        for i in range(10): # running loop for creating multiple arcs
            pygame.draw.arc(screen,(0,0,arc_color),rect,math.radians(angle),math.radians(angle+100),arc_width) # inner arc1
            pygame.draw.arc(screen,(0,0,arc_color),rect,math.radians(angle+110),math.radians(angle+220),arc_width) # inner arc2
            pygame.draw.arc(screen,(0,0,arc_color),rect,math.radians(angle+230),math.radians(angle+350),arc_width) # inner arc3

            pygame.draw.arc(screen,(0,0,arc_color),rect1,math.radians(angle1),math.radians(angle1+170),arc_width) # outer arc1
            pygame.draw.arc(screen,(0,0,arc_color),rect1,math.radians(angle1+180),math.radians(angle1+350),arc_width) # outer arc2
            arc_width -= 1 # decreasing arc width
            arc_color -= 10 # decreasing blue color lightness

# -------------------------checking parameter---------------------------------------------------------------------------

        if ai_status == "input": # floating and spinning inner arcs
            angle += 2
        
        elif ai_status == "process": # floating and spinning both arcs
            angle += 2
            angle1 -= 2
        
        elif ai_status == "output": # floating and spinning outer arcs
            angle1 -= 2
        
        elif ai_status == "idle": # floating circle
            pass

        else: # returning None if input is invalid
            return

# ---------------------------updating and exiting pygame------------------------------------------------------------------

        pygame.display.update() # updating display
        clock.tick(fps)

    pygame.quit() # terminating pygame

# =========================creating and starting thread for ai_avatar function================================================

ai_thread = threading.Thread(
    target=ai_avatar)

ai_thread.start() # starting the ai_avatar function thread

# =================================select_model===============================================================================

def select_model(): # function to select 

    global ai_status
    
    ai_status = "idle" 

    global model # declaring model as global variable to use it outside the function

# ----------------------------------displaying models----------------------------------------------------------------------

    print("""\nModels:
Type "1" for - openai/gpt-oss-120b
Type "2" for - openai/gpt-oss-20b""") # displaying model options

    ai_status = "input"

# ----------------------------------checking user input and selecting model---------------------------------------------------

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

# ====================================system================================================================================

def system(): # function to select system instructions

    global ai_status

    ai_status = "input"

# ---------------------------------------taking system instructions---------------------------------------------------------

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

# ---------------------------appeding system instructions-------------------------------------------------------------------

        context[0] = ({"role": "system", "content": system_instructions}) # appending system instructions to context
        return

# ============================================change_model==================================================================    

def change_model():

    global model # declaring model as global variable to use it outside the function
    global ai_status

# ---------------------------checking and changing model---------------------------------------------------------------------

    if model == "openai/gpt-oss-120b": # checking model and printing total tokens usage of model 1
        print("\nTotal tokens usage of model 1 is very high.")

    elif model == "openai/gpt-oss-20b": # checking model and printing total tokens usage of model 2
        print("\nTotal tokens usage of model 2 is very high.")

    print("\nYou can continue the session by changing the model.")

    ai_status = "input"

    while True: # looping until user input is valid

        change = input("\nDo you want to change the model? (y/n): ") # taking user input to change model

        if change.lower() == "y": # checking user input

            if model == "openai/gpt-oss-120b": # changing model
                model = "openai/gpt-oss-20b"

            elif model == "openai/gpt-oss-20b":
                model = "openai/gpt-oss-120b"
                
            print(f"\n⇄  Model changed to {model}.")
            return model # returning new model name

# ----------------------------exiting if user wants to leave---------------------------------------------------------------

        elif change.lower() == "n": # checking if user want to exit the session
            return "//exit"
        
        else:
            print("\n⊘  Invalid input.") # skipping the loop if input is invalid

# ================================posting=================================================================================

def posting(model,context): # function to send user messages and generate AI response

    global ai_status

    ai_status = "input"

# -------------------------taking and checking user inputs--------------------------------------------------------------------

    user_message = input("""\nType your message
Or type '//exit' to exit 
Or type '//view commands' to view commands: """) # taking user message

    if user_message.lower() == "//view commands":
        print("\nCOMMNADS BELOW:") # displaying all commands
        user_message = input("""\nType '//change model' to change the model 
Or type '//show model' to show the current model
Or type '//change system' to change the system instructions
Or type '//show system' to show the current system instructions
Or type '//delete history' to delete your conversation history
Or type '//reset' to delete all conversation history and change system instructions to default: """)

        if (user_message.lower() == "//change model" or # checking user_message
            user_message.lower() == "//show model" or
            user_message.lower() == "//change system" or
            user_message.lower() == "//show system" or
            user_message.lower() == "//delete history" or
            user_message.lower() == "//reset"):

            user_message += "/"
            return user_message,None # returning user message and None

        else:
            print("\n⊘  Invalid input.")
            return None # returning None to skip the loop

    if user_message.lower() == "//exit": # checking user_message
        return user_message,None # returning user message and None

    if (user_message.lower() == "//change model" or # checking user_message
        user_message.lower() == "//show model" or
        user_message.lower() == "//change system" or
        user_message.lower() == "//show system" or
        user_message.lower() == "//delete history" or
        user_message.lower() == "//reset"):
        print('\nIf you want to use this commands  type "//view commands": ')
        return None

    
    
   
# --------------------------------sending user messages and generating AI response----------------------------------------------

    ai_status = "process"

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
        
# -------------------------------handling errors-----------------------------------------------------------------------------

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

# =======================================operations=========================================================================

def operations(): # function to perform operations like sending user messages, generating AI response, changing model and system instructions

    global ai_status

    ai_status = "idle"

    global total_tokens1 # declaring total_tokens1 as global variable to count token usage of model 1
    global total_tokens2 # declaring total_tokens2 as global variable to count token usage of model 2
    global context # declaring context as global variable to change and delete old messages

    while True: # looping until user wants to exit the session

# -----------------checking whether user had hit the limit---------------------------------------------------------------------

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

# -------------------checking user input---------------------------------------------------------------------------------

        if user_message.lower() == "//exit": # checking if user wants to exit the session
            print("\n⇥  Session exited. All your data will be deleted.")
            return "//exit"

        elif user_message.lower() == "//change model/": # checking if user wants to change the model
            select_model() # calling select_model() function to change the model
            continue

        elif user_message.lower() == "//show model/": # checking if user wants to show the current model
            print(f"\n▣ Current model: {model}") # printing current model
            continue

        elif user_message.lower() == "//change system/": # checking if user wants to change the system instructions
            system() # calling system() function to change the system instructions
            continue

        elif user_message.lower() == "//show system/": # checking if user wants to show the current system instructions
            print(f"\n▤  Current system instructions: {context[0]['content']}") # printing current system instructions
            continue

        elif user_message.lower() == "//delete history/":
            del context[1:]
            print("\n🗑️  All conversation history is deleted.")
            continue

        elif user_message.lower() == "//reset/":
            print("\n↻  All conversation history is deleted and system instructions changed to default.")
            del context[1:]
            context[0] = ({"role": "system", "content": "Strictly use neutral(emotionless), calm, robotic, concise, analytical, factual and balanced energy tone. *Your name is 'Measured'."})
            continue

# --------------------------handling errors-----------------------------------------------------------------------------------

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
# -------------------------------appeding and deleting ai and user responses---------------------------------------------------- 
#        
        context.append({"role": "user", "content": user_message}) # appending user message
        context.append({"role": "assistant", "content": ai_response}) # appending ai response

        if len(context) > 21: # deleting oldest user-AI pair if context length exceeds 21
            del context[1:(len(context)-20)]

        return ai_response

# ===================================display=================================================================================

def display(ai_response,total_tokens1,total_tokens2): # function to display AI response and total tokens usage

    global ai_status

    ai_status = "output"

    print(f"\n◈ AI's RESPONSE:") # printing AI response (simulated streaming effect)

    for ch in ai_response:
        print(ch,end="",flush=True)
        time.sleep(0.01)

    print(f"\n\n● TOTAL TOKENS USED: {total_tokens1 + total_tokens2}") # printing total tokens usage 
    print(f"● TOTAL TOKENS OF MODEL 1: {total_tokens1}") # printing total tokens usage of model 1
    print(f"● TOTAL TOKENS OF MODEL 2: {total_tokens2}") # printing total tokens usage of model 2

# ===================================calling select_model and system functions=============================================

select_model() # calling select_model() function to select model
system() # calling system() function to select system instructions

 # =================================main loop==============================================================================

while True: # looping until user wants to exit the session

    ai_status = "idle"

    ai_response = operations() # calling operations() function to perform operations like sending user messages, generating AI response, changing model and system instructions
    if ai_response == "//exit": # checking if user wants to exit the session
        break

    display(ai_response,total_tokens1,total_tokens2) # calling display() function to display AI response and total tokens usage
# ======================================terminating ai_avatar thread=======================================================

ai_running = False
