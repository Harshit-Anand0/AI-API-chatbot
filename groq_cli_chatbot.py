import requests
import os
import time
import threading
import pygame
import math


# =========================================================
# GLOBAL VARIABLES
# =========================================================

total_tokens1 = 0
total_tokens2 = 0

apikey = os.getenv("GroqApiKey")

context = [None]

model = None

# Avatar control
avatar_status = "idle"
avatar_running = True


# =========================================================
# AI AVATAR
# =========================================================

def ai_avatar():

    global avatar_status
    global avatar_running

    pygame.init()

    width = 600
    height = 700

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("AI Avatar")

    # Circle variables
    move = 0
    circle_y = height / 2
    circle_x = width / 2
    size = 150

    # Arc variables
    angle = 0
    angle1 = 0
    arc_size = size

    # Speed
    fps = 60
    clock = pygame.time.Clock()

    while avatar_running:

        # -------------------------------------------------
        # PYGAME EVENTS
        # -------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                avatar_running = False


        # -------------------------------------------------
        # SCREEN
        # -------------------------------------------------

        screen.fill((0, 0, 0))


        # -------------------------------------------------
        # CIRCLE
        # -------------------------------------------------

        color = 0
        size = 150

        for i in range(150):

            pygame.draw.circle(
                screen,
                (0, 0, int(color)),
                (int(circle_x), int(circle_y)),
                size
            )

            color += 1.5
            size -= 1


        # -------------------------------------------------
        # FLOATING
        # -------------------------------------------------

        circle_y = 250 + math.sin(math.radians(move)) * 25

        move += 1


        # -------------------------------------------------
        # ARCS
        # -------------------------------------------------

        rect = (
            circle_x - arc_size - 30,
            circle_y - arc_size - 30,
            360,
            360
        )

        rect1 = (
            circle_x - arc_size - 60,
            circle_y - arc_size - 60,
            420,
            420
        )

        arc_width = 15
        arc_color = 100


        for i in range(10):

            # Inner arc 1
            pygame.draw.arc(
                screen,
                (0, 0, int(arc_color)),
                rect,
                math.radians(angle),
                math.radians(angle + 100),
                arc_width
            )

            # Inner arc 2
            pygame.draw.arc(
                screen,
                (0, 0, int(arc_color)),
                rect,
                math.radians(angle + 110),
                math.radians(angle + 220),
                arc_width
            )

            # Inner arc 3
            pygame.draw.arc(
                screen,
                (0, 0, int(arc_color)),
                rect,
                math.radians(angle + 230),
                math.radians(angle + 350),
                arc_width
            )

            # Outer arc 1
            pygame.draw.arc(
                screen,
                (0, 0, int(arc_color)),
                rect1,
                math.radians(angle1),
                math.radians(angle1 + 170),
                arc_width
            )

            # Outer arc 2
            pygame.draw.arc(
                screen,
                (0, 0, int(arc_color)),
                rect1,
                math.radians(angle1 + 180),
                math.radians(angle1 + 350),
                arc_width
            )

            arc_width -= 1
            arc_color -= 10


        # -------------------------------------------------
        # AVATAR STATUS
        # -------------------------------------------------

        status = avatar_status.lower()


        if status == "input":

            angle += 2


        elif status == "processing":

            angle += 2
            angle1 -= 2


        elif status == "output":

            angle1 -= 2


        elif status == "idle":

            pass


        # -------------------------------------------------
        # DISPLAY
        # -------------------------------------------------

        pygame.display.update()

        clock.tick(fps)


    pygame.quit()


# =========================================================
# AVATAR THREAD
# =========================================================

avatar_thread = threading.Thread(
    target=ai_avatar,
    daemon=True
)

avatar_thread.start()


# =========================================================
# SELECT MODEL
# =========================================================

def select_model():

    global model
    global avatar_status

    avatar_status = "input"

    print("""
Models:

Type "1" for - openai/gpt-oss-120b

Type "2" for - openai/gpt-oss-20b
""")


    while True:

        model = input("\nEnter model: ")


        if model == "1":

            model = "openai/gpt-oss-120b"

            print(f"\n✓  {model} selected")

            avatar_status = "idle"

            return


        elif model == "2":

            model = "openai/gpt-oss-20b"

            print(f"\n✓  {model} selected")

            avatar_status = "idle"

            return


        else:

            print("\n⊘  Invalid input")


# =========================================================
# SYSTEM INSTRUCTIONS
# =========================================================

def system():

    global avatar_status

    avatar_status = "input"


    while True:

        system_instructions = input(
            "\nEnter system instructions "
            '(or type "//default" to choose default system instruction): '
        )


        if not system_instructions or system_instructions.isspace():

            print("\n⊘  Invalid input")

            continue


        elif system_instructions.lower() == "//default":

            system_instructions = (
                "Strictly use neutral(emotionless), calm, robotic, "
                "concise, analytical, factual and balanced energy tone. "
                "Your name is 'Measured'."
            )

            print("\n◆  Default system instructions added successfully.")


        else:

            print("\n⇄  System instructions changed successfully.")


        context[0] = {
            "role": "system",
            "content": system_instructions
        }

        avatar_status = "idle"

        return


# =========================================================
# CHANGE MODEL
# =========================================================

def change_model():

    global model
    global avatar_status

    avatar_status = "input"


    if model == "openai/gpt-oss-120b":

        print("\nTotal tokens usage of model 1 is very high.")


    elif model == "openai/gpt-oss-20b":

        print("\nTotal tokens usage of model 2 is very high.")


    print("\nYou can continue the session by changing the model.")


    while True:

        change = input("\nDo you want to change the model? (y/n): ")


        if change.lower() == "y":

            if model == "openai/gpt-oss-120b":

                model = "openai/gpt-oss-20b"


            elif model == "openai/gpt-oss-20b":

                model = "openai/gpt-oss-120b"


            print(f"\n⇄  Model changed to {model}.")

            avatar_status = "idle"

            return model


        elif change.lower() == "n":

            avatar_status = "idle"

            return "//exit"


        else:

            print("\n⊘  Invalid input.")


# =========================================================
# POSTING
# =========================================================

def posting(model, context):

    global avatar_status

    avatar_status = "input"


    user_message = input(
        """\nType your message

Or type '//exit' to exit 

Or type '//view commands' to view commands: """
    )


    # -----------------------------------------------------
    # VIEW COMMANDS
    # -----------------------------------------------------

    if user_message.lower() == "//view commands":

        print("\nCOMMANDS BELOW:")


        user_message = input(
            """\nType '//change model' to change the model

Or type '//show model' to show the current model

Or type '//change system' to change the system instructions

Or type '//show system' to show the current system instructions

Or type '//delete history' to delete your conversation history

Or type '//reset' to delete all conversation history and change system instructions to default: """
        )


        if (
            user_message.lower() == "//change model"
            or
            user_message.lower() == "//show model"
            or
            user_message.lower() == "//change system"
            or
            user_message.lower() == "//show system"
            or
            user_message.lower() == "//delete history"
            or
            user_message.lower() == "//reset"
        ):

            user_message += "/"

            avatar_status = "idle"

            return user_message, None


        else:

            print("\n⊘  Invalid input.")

            avatar_status = "idle"

            return None


    # -----------------------------------------------------
    # EXIT
    # -----------------------------------------------------

    if user_message.lower() == "//exit":

        avatar_status = "idle"

        return user_message, None


    # -----------------------------------------------------
    # PROCESSING
    # -----------------------------------------------------

    avatar_status = "processing"


    try:

        response = requests.post(

            "https://api.groq.com/openai/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {apikey}"
            },

            json={

                "model": model,

                "messages":
                    context +
                    [
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ],

                "max_completion_tokens": 700,

                "temperature": 1,

                "top_p": 1
            },

            timeout=20
        )


        # -------------------------------------------------
        # HTTP ERROR
        # -------------------------------------------------

        if response.status_code > 399:

            print(
                f"\n#️⃣  STATUS CODE: {response.status_code}"
            )

            print(
                f"\n⚠  HTTP ERROR(DETAILED): {response.text}"
            )


        response.raise_for_status()


        final_response = response.json()


        avatar_status = "idle"

        return user_message, final_response


    # -----------------------------------------------------
    # ERRORS
    # -----------------------------------------------------

    except requests.exceptions.HTTPError as e:

        print(f"\n⚠  HTTP Error: {e}")

        avatar_status = "idle"


    except requests.exceptions.JSONDecodeError as e:

        print(f"\n⚠  Invalid JSON error: {e}")

        avatar_status = "idle"


    except requests.exceptions.ConnectTimeout as e:

        print(f"\n⚠  Connect timed out error: {e}")

        avatar_status = "idle"


    except requests.exceptions.ReadTimeout as e:

        print(f"\n⚠  Read timed out error: {e}")

        avatar_status = "idle"


    except requests.exceptions.Timeout as e:

        print(f"\n⚠  Timed out error: {e}")

        avatar_status = "idle"


    except requests.exceptions.ConnectionError as e:

        print(f"\n⚠  Connection error: {e}")

        avatar_status = "idle"


    except Exception as e:

        print(f"\n⚠  New error found: {e}")

        avatar_status = "idle"


# =========================================================
# OPERATIONS
# =========================================================

def operations():

    global total_tokens1
    global total_tokens2
    global context
    global avatar_status


    while True:

        # -------------------------------------------------
        # TOTAL TOKEN LIMIT
        # -------------------------------------------------

        if total_tokens1 + total_tokens2 >= 180000:

            print(
                "\n🛑  Token usage of both models has reached the limit. "
                "Session exited. All your data will be deleted."
            )

            return "//exit"


        # -------------------------------------------------
        # MODEL TOKEN LIMIT
        # -------------------------------------------------

        if (
            (
                model == "openai/gpt-oss-120b"
                and
                total_tokens1 >= 90000
            )
            or
            (
                model == "openai/gpt-oss-20b"
                and
                total_tokens2 >= 90000
            )
        ):

            change_model_output = change_model()


            if change_model_output.lower() == "//exit":

                print(
                    "\n⇥  Session exited. "
                    "All your data will be deleted."
                )

                return "//exit"


        # -------------------------------------------------
        # POSTING
        # -------------------------------------------------

        output2 = posting(model, context)


        if not output2:

            continue


        user_message, final_response = output2


        # -------------------------------------------------
        # USER EXIT
        # -------------------------------------------------

        if user_message.lower() == "//exit":

            print(
                "\n⇥  Session exited. "
                "All your data will be deleted."
            )

            return "//exit"


        # -------------------------------------------------
        # COMMANDS
        # -------------------------------------------------

        elif user_message.lower() == "//change model/":

            select_model()

            continue


        elif user_message.lower() == "//show model/":

            print(f"\n▣ Current model: {model}")

            continue


        elif user_message.lower() == "//change system/":

            system()

            continue


        elif user_message.lower() == "//show system/":

            print(
                f"\n▤  Current system instructions: "
                f"{context[0]['content']}"
            )

            continue


        elif user_message.lower() == "//delete history/":

            del context[1:]

            print("\n🗑️  All conversation history is deleted.")

            continue


        elif user_message.lower() == "//reset/":

            print(
                "\n↻  All conversation history is deleted "
                "and system instructions changed to default."
            )


            del context[1:]


            context[0] = {
                "role": "system",
                "content":
                    "Strictly use neutral(emotionless), calm, "
                    "robotic, concise, analytical, factual and "
                    "balanced energy tone. "
                    "Your name is 'Measured'."
            }

            continue


        # -------------------------------------------------
        # EXTRACT AI RESPONSE
        # -------------------------------------------------

        try:

            ai_response = (
                final_response["choices"][0]["message"]["content"]
            )


            if model == "openai/gpt-oss-120b":

                total_tokens1 += (
                    final_response["usage"]["total_tokens"]
                )


            elif model == "openai/gpt-oss-20b":

                total_tokens2 += (
                    final_response["usage"]["total_tokens"]
                )


        except KeyError as e:

            print(f"\n⚠  Key error occured: {e}")

            continue


        except TypeError as e:

            print(f"\n⚠  Type error occured: {e}")

            continue


        # -------------------------------------------------
        # UPDATE CONTEXT
        # -------------------------------------------------

        context.append(
            {
                "role": "user",
                "content": user_message
            }
        )


        context.append(
            {
                "role": "assistant",
                "content": ai_response
            }
        )


        if len(context) > 21:

            del context[1:(len(context) - 20)]


        return ai_response


# =========================================================
# DISPLAY
# =========================================================

def display(
    ai_response,
    total_tokens1,
    total_tokens2
):

    global avatar_status

    avatar_status = "output"


    print("\n◈ AI's RESPONSE:")


    for ch in ai_response:

        print(
            ch,
            end="",
            flush=True
        )

        time.sleep(0.01)


    print(
        f"\n\n● TOTAL TOKENS USED: "
        f"{total_tokens1 + total_tokens2}"
    )


    print(
        f"● TOTAL TOKENS OF MODEL 1: "
        f"{total_tokens1}"
    )


    print(
        f"● TOTAL TOKENS OF MODEL 2: "
        f"{total_tokens2}"
    )


    avatar_status = "idle"


# =========================================================
# START CHATBOT
# =========================================================

select_model()

system()


while True:

    ai_response = operations()


    if ai_response == "//exit":

        break


    display(
        ai_response,
        total_tokens1,
        total_tokens2
    )


# =========================================================
# SHUTDOWN AVATAR
# =========================================================

avatar_running = False

avatar_thread.join(timeout=2)

print("\nChatbot terminated.")
