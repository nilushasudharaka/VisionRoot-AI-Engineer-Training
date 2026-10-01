import os

from dotenv import load_dotenv
from google import genai

from tools import (
    check_room_availability,
    calculate_booking_price
)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured.")


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=GEMINI_API_KEY)


# ============================================================
# AGENT INSTRUCTIONS
# ============================================================

SYSTEM_INSTRUCTION = """
You are a Hotel Assistant AI Agent.

Your job is to help users with:

1. Hotel room availability
2. Hotel booking price calculations

You have access to ONLY these two tools:

- check_room_availability
- calculate_booking_price

Tool selection rules:

- If the user asks whether a room is available,
  use check_room_availability.

- If the user asks for the price of a room,
  use calculate_booking_price.

- If the user asks both availability and price,
  you may use both tools.

- Never invent room availability or prices.

- Never perform actions outside the available tools.

- Do not execute arbitrary Python code.

- If the user asks for an unsupported action,
  explain that you can only help with room availability
  and price calculations.

Always provide a clear final answer after using the tools.
"""


# ============================================================
# CREATE CHAT SESSION
# ============================================================

chat = client.chats.create(
    model="gemini-3.8-flash",
    config={
        "system_instruction": SYSTEM_INSTRUCTION,
        "tools": [
            check_room_availability,
            calculate_booking_price
        ]
    }
)


# ============================================================
# RUN AGENT
# ============================================================

def run_agent(user_request):

    response = chat.send_message(user_request)

    return response.text


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("HOTEL ASSISTANT AI AGENT")
    print("=" * 60)

    print("\nAvailable capabilities:")
    print("- Check room availability")
    print("- Calculate booking price")
    print("\nType 'exit' to quit.")

    while True:

        user_request = input("\nYou: ").strip()

        if user_request.lower() in ["exit", "quit"]:
            print("Agent: Goodbye!")
            break

        if not user_request:
            print("Agent: Please enter a request.")
            continue

        try:

            answer = run_agent(user_request)

            print("\nAgent:")
            print(answer)

        except Exception as e:

            print("\nAgent Error:")
            print(e)


if __name__ == "__main__":
    main()