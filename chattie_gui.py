import tkinter as tk
from tkinter import scrolledtext
import random
import datetime
import time
import threading

# ------------------ Intent-based Bot Memory ------------------
user_name = None  # Store user's name if provided

# ------------------ Intent Dictionary ------------------
intents = {
    "greeting": {
        "keywords": ["hi", "hello", "hey", "good morning", "good evening"],
        "responses": ["Hello! 😊", "Hey there! 👋", "Hi, how can I help you today? 🤖"]
    },
    "how_are_you": {
        "keywords": ["how are you", "how's it going", "what's up"],
        "responses": ["I'm good, thanks for asking! 😄", "Doing great! What about you? 💪"]
    },
    "name_query": {
        "keywords": ["your name", "who are you"],
        "responses": ["I'm RuleBot 3.5 – your AI buddy. 🤖"]
    },
    "capabilities": {
        "keywords": ["what can you do", "help", "features"],
        "responses": ["I can chat, tell the time, remember your name, and make you smile! 😄"]
    },
    "time": {
        "keywords": ["time", "current time", "tell me the time"],
        "responses": [f"The current time is {datetime.datetime.now().strftime('%I:%M %p')} 🕒"]
    },
    "thanks": {
        "keywords": ["thanks", "thank you", "thx"],
        "responses": ["You're welcome! 😊", "Anytime! 🙌", "Glad to help! 👍"]
    },
    "bye": {
        "keywords": ["bye", "goodbye", "see you"],
        "responses": ["Goodbye! 👋", "Take care! 💖", "See you later! 😄"]
    },
    "jokes": {
        "keywords": ["joke", "make me laugh", "funny"],
        "responses": [
            "Why did the computer go to the doctor? Because it had a virus! 😂",
            "I would tell you a UDP joke... but you might not get it. 😅",
            "Why don't robots panic? Because they have nerves of steel! 🤖"
        ]
    },
    "nice": {
        "keywords": ["nice", "good", "haha", "lol", "funny"],
        "responses": ["happy that you liked😄"]
    },
    "mood_sad": {
        "keywords": ["sad", "depressed", "unhappy", "upset"],
        "responses": [
            "I'm here for you. Everything will be okay. 💖",
            "Sending you virtual hugs 🤗",
            "Tough times don’t last, but tough people do 💪"
        ]
    },
    "mood_happy": {
        "keywords": ["happy", "excited", "joyful", "glad"],
        "responses": ["Yay! I’m happy to hear that! 😄", "That’s awesome! Let’s keep the good vibes going 🎉"]
    }
}

# ------------------ Intent Detection ------------------
def get_intent(user_input):
    user_input = user_input.lower()
    for intent, data in intents.items():
        for keyword in data["keywords"]:
            if keyword in user_input:
                return intent
    return None

# ------------------ Response Generator ------------------
def get_bot_response(user_input):
    global user_name

    user_input = user_input.lower()

    if "my name is" in user_input:
        user_name = user_input.split("my name is")[-1].strip().capitalize()
        return f"Nice to meet you, {user_name}! 😄"

    if "what's my name" in user_input or "do you remember me" in user_input:
        if user_name:
            return f"Of course! You're {user_name} 😎"
        else:
            return "I don't know your name yet! Tell me by saying 'my name is ...'"

    intent = get_intent(user_input)
    if intent:
        return random.choice(intents[intent]["responses"])
    else:
        return "Hmm... I didn’t quite understand that. Can you rephrase it? 🤔"

# ------------------ Typing Effect Simulation ------------------
def bot_typing_effect(text):
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "RuleBot is typing...\n")
    chat_area.update()
    time.sleep(0.8)
    chat_area.delete("end-2l", "end-1l")  # Remove "typing..." line
    chat_area.insert(tk.END, "RuleBot: " + text + "\n\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

# ------------------ Message Sending Logic ------------------
def send_message():
    user_input = user_entry.get()
    if user_input.strip() == "":
        return

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "You: " + user_input + "\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

    user_entry.delete(0, tk.END)

    # Use threading so UI doesn’t freeze during typing delay
    threading.Thread(target=lambda: bot_typing_effect(get_bot_response(user_input))).start()

# ------------------ Time-Based Greeting ------------------
def time_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning! 🌅"
    elif hour < 18:
        return "Good afternoon! ☀️"
    else:
        return "Good evening! 🌙"

# ------------------ GUI Setup ------------------
# ------------------ Main Window ------------------

window = tk.Tk()
window.title("RuleBot Chat")
window.geometry("500x600")              # slightly bigger for better space
window.config(bg="white")               # white background

chat_area = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    width=60,
    height=25,
    font=("Arial", 11),
    bg="white",                         # white background for chat area
    fg="#333333",                       # dark gray text for better readability
    bd=0,                               # no border
    padx=10, pady=10
)
chat_area.config(state=tk.DISABLED)
chat_area.pack(pady=(10, 5))

user_entry = tk.Entry(
    window,
    width=45,
    font=("Arial", 12),
    bg="white",                         # white input box
    fg="#000000",                       # black text
    bd=1,
    relief=tk.GROOVE
)
user_entry.pack(padx=10, pady=5, side=tk.LEFT)

send_button = tk.Button(
    window,
    text="Send",
    command=send_message,
    font=("Arial", 12),
    bg="#0078D7",                       # blue send button (like Microsoft's Fluent UI)
    fg="white",
    activebackground="#005a9e",
    activeforeground="white",
    width=10,
    relief=tk.FLAT,
    cursor="hand2"
)
send_button.pack(pady=5, padx=5, side=tk.RIGHT)

# Welcome message
chat_area.config(state=tk.NORMAL)
chat_area.insert(tk.END, f"RuleBot: {time_greeting()}\nRuleBot: Ask me anything! Type 'bye' to end the chat.\n\n")
chat_area.config(state=tk.DISABLED)

window.mainloop()