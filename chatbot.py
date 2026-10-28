
import ollama
import csv
import os
from datetime import datetime

# Configuration
MODEL_NAME = "llama3.2"
HISTORY_FILE = "dataset/chat_history.csv"

# Create CSV file with headers if it does not exist
os.makedirs("dataset", exist_ok=True)

if not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0:
    with open(HISTORY_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "user_message", "bot_response"])

# Store conversation context
messages = []

print("=" * 45)
print("       WEEK 9 - AI CHATBOT")
print("=" * 45)
print("Type 'exit' to stop the chatbot.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye! Have a nice day!")
        break

    if not user_input:
        print("Chatbot: Please enter a message.")
        continue

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages
        )

        bot_reply = response["message"]["content"]

        messages.append({
            "role": "assistant",
            "content": bot_reply
        })

        print(f"\nChatbot: {bot_reply}\n")

        # Save conversation to CSV
        with open(
            HISTORY_FILE, "a", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_input,
                bot_reply
            ])

    except Exception as error:
        print(f"\nError: {error}")
        print("Check whether Ollama is running and the model is available.\n")
        messages.pop()
